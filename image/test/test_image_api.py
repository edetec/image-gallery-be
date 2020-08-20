from http import HTTPStatus

import pytest

from image.models import Image


@pytest.yield_fixture()
def images(session):
    image1 = Image(
        file_name="file1.jpg",
        thumbnail_name="thumbnail/file1.jpg",
        description="description file 1",
        format="JPG",
        dimensions="800x600")
    image2 = Image(
        file_name="file2.jpg",
        thumbnail_name="thumbnail/file2.jpg",
        description="description file 2",
        format="JPG",
        dimensions="800x600")
    image3 = Image(
        file_name="file3.jpg",
        thumbnail_name="thumbnail/file3.jpg",
        description="description file 3",
        format="JPG",
        dimensions="900x600")
    session.add(image1)
    session.add(image2)
    session.add(image3)
    yield image1
    for image in Image.query.all():
        session.delete(image)


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
