from typing import BinaryIO, Dict, Tuple

import pytest
from fastapi.testclient import TestClient
from rq import Queue

from app import db
from app.api import app

db.queue = Queue(is_async=False, connection=db.redis_conn)

square_images = ['puppy1.jpg', 'puppy2.jpg', 'puppy3.jpg']
incorrect_files = [
    'not_square1.jpg',
    'not_square2.jpg',
    'not_square3.jpg',
    'some_text_file',
]


def make_file_for_sending(filename: str) -> Dict[str, Tuple[str, BinaryIO, str]]:
    return {
        'file': ('filename', open(f'tests/input_pics/{filename}', 'rb'), 'image/jpeg'),
    }


@pytest.fixture()
def client():
    return TestClient(app)


@pytest.fixture(params=square_images)
def square_image_file(request):
    return make_file_for_sending(request.param)


@pytest.fixture(params=incorrect_files)
def incorrect_file_name(request):
    return make_file_for_sending(request.param)


@pytest.fixture(params=square_images)
def square_image_filename(request):
    return request.param
