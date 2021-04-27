import pytest
from PIL import ImageChops

from app.crud import Status
from app.routing import ImageSize
from tests.converters import convert_bytes_to_rgb_image, convert_expected_image_to_rgb


def test_status_is_done(client, square_image_file):
    response_post_request = client.post('/tasks', files=square_image_file)
    job_id = response_post_request.json()

    response_get_request = client.get(f'/tasks/{job_id}')
    status = Status(response_get_request.json())

    assert response_post_request.status_code == 201
    assert response_get_request.status_code == 200
    assert status == Status.done


def test_incorrect_file_input(client, incorrect_file_name):
    response = client.post('/tasks', files=incorrect_file_name)

    assert response.status_code == 422
    assert 'detail' in response.json()


@pytest.mark.parametrize(
    'img_size', [ImageSize.size_original, ImageSize.size_32, ImageSize.size_64]
)
def test_job_result(client, square_image_filename, img_size):
    response_post_request = client.post(
        '/tasks',
        files={
            'file': (
                'filename',
                open(f'tests/input_pics/{square_image_filename}', 'rb'),
                'image/jpeg',
            )
        },
    )
    job_id = response_post_request.json()

    response_get_image = client.get(f'/tasks/{job_id}/image?size={img_size}')
    image_bytes = response_get_image.content

    rgb_response = convert_bytes_to_rgb_image(image_bytes)
    rgb_expected = convert_expected_image_to_rgb(
        filename=square_image_filename, img_size=img_size.value
    )

    diff = ImageChops.difference(rgb_expected, rgb_response)
    assert not diff.getbbox()


@pytest.mark.parametrize(
    ('job_id', 'expected_code'), [('invalid', 422), ('10000000000000', 404)]
)
def test_get_job_status_incorrect_args(job_id, expected_code, client):
    response = client.get(f'/tasks/{job_id}')

    assert response.status_code == expected_code
    assert 'detail' in response.json()


@pytest.mark.parametrize(
    ('job_id', 'img_size', 'expected_code'),
    [('invalid', '32', 422), ('10000000000000', '32', 404), ('1', 'invalid', 422)],
)
def test_job_result_incorrect_args(job_id, expected_code, client, img_size):
    response = client.get(f'/tasks/{job_id}/image?size={img_size}')

    assert response.status_code == expected_code
    assert 'detail' in response.json()
