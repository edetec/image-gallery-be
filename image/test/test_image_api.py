import uuid
from http import HTTPStatus
from pathlib import Path

import pytest

from image.models import ImageModel


@pytest.yield_fixture()
def images(session):
    image1 = ImageModel(
        file_path="file1.jpg",
        thumbnail_path="thumbnail/file1.jpg",
        description="description file 1",
        format="jpg",
        dimensions="800x600")
    image2 = ImageModel(
        file_path="file2.jpg",
        thumbnail_path="thumbnail/file2.jpg",
        description="description file 2",
        format="jpg",
        dimensions="800x600")
    image3 = ImageModel(
        file_path="file3.jpg",
        thumbnail_path="thumbnail/file3.jpg",
        description="description file 3",
        format="jpg",
        dimensions="900x600")
    session.add(image1)
    session.add(image2)
    session.add(image3)
    yield image1
    for image in ImageModel.query.all():
        session.delete(image)


@pytest.yield_fixture
def photo1():
    file_name = 'photo 1.png'
    file_path = Path(__file__).parent.joinpath('assets', file_name)
    with open(file_path, 'rb') as file:
        yield file, file_name


@pytest.yield_fixture
def photo2():
    file_name = 'photo 1.png'
    file_path = Path(__file__).parent.joinpath('assets', file_name)
    with open(file_path, 'rb') as file:
        yield file, file_name


@pytest.yield_fixture
def tmp_app_dir(test_client, tmpdir):
    config = test_client.application.config
    ROOT_DIR = config['ROOT_DIR']
    config['ROOT_DIR'] = tmpdir
    Path(tmpdir).joinpath(config['IMAGES_PATH']).mkdir(parents=True)
    yield tmpdir
    config['ROOT_DIR'] = ROOT_DIR


def test_get_all_images(test_client, images, data_regression):
    response = test_client.get("/api/v1/image/")
    assert response.status_code == HTTPStatus.OK
    data_regression.check(response.json)


def test_get_images_with_filter_param(test_client, images, data_regression):
    filter_param = "file 1"
    response = test_client.get(f"/api/v1/image/?description={filter_param}")
    assert response.status_code == HTTPStatus.OK
    assert len(response.json) == 1
    data_regression.check(response.json)


def test_get_all_image_dimensions(test_client, images, data_regression):
    response = test_client.get(f"/api/v1/image/dimensions/")
    assert response.status_code == HTTPStatus.OK
    data_regression.check(response.json)


def test_image_upload(test_client, photo1, tmp_app_dir, monkeypatch, data_regression):
    monkeypatch.setattr(uuid, "uuid4", lambda: 'unique-file-name')

    response = test_client.post('/api/v1/image/', buffered=True,
                                content_type='multipart/form-data',
                                data={
                                    'description': 'Photo 1 description',
                                    'file': photo1
                                })
    assert response.status_code == HTTPStatus.CREATED
    image_dict = response.json
    assert Path(tmp_app_dir).joinpath(image_dict['file_path']).exists()
    assert Path(tmp_app_dir).joinpath(image_dict['thumbnail_path']).exists()
    data_regression.check(image_dict)


def test_image_update(test_client, photo1, photo2, tmp_app_dir, monkeypatch, data_regression):
    response = test_client.post('/api/v1/image/', buffered=True,
                                content_type='multipart/form-data',
                                data={
                                    'description': 'Photo 2 description',
                                    'file': photo1
                                })
    assert response.status_code == HTTPStatus.CREATED
    image1_dict = response.json
    assert Path(tmp_app_dir).joinpath(image1_dict['file_path']).exists()
    assert Path(tmp_app_dir).joinpath(image1_dict['thumbnail_path']).exists()

    image1_id = image1_dict['id']
    monkeypatch.setattr(uuid, "uuid4", lambda: 'unique-file-name')
    response = test_client.put(f'/api/v1/image/{image1_id}', buffered=True,
                               content_type='multipart/form-data',
                               data={
                                   'description': 'Photo 2 description',
                                   'file': photo2
                               })
    assert response.status_code == HTTPStatus.OK
    image_dict = response.json
    assert Path(tmp_app_dir).joinpath(image_dict['file_path']).exists()
    assert Path(tmp_app_dir).joinpath(image_dict['thumbnail_path']).exists()
    assert not Path(tmp_app_dir).joinpath(image1_dict['file_path']).exists()
    assert not Path(tmp_app_dir).joinpath(image1_dict['thumbnail_path']).exists()
    data_regression.check(image_dict)
