from http import HTTPStatus


def test_get_all_images(test_client):
    response = test_client.get("/api/v1/image/")
    assert response.status_code == HTTPStatus.OK
