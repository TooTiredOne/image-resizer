import base64
from enum import Enum
from io import BytesIO
from typing import Optional

from PIL import Image
from rq.exceptions import NoSuchJobError
from rq.job import Job, JobStatus

from app import db


class Status(Enum):
    done = 'DONE'
    waiting = 'WAITING'
    in_progress = 'IN_PROGRESS'
    failed = 'FAILED'


# pylint: disable=no-member


def get_image_from_db(job_id: int, size: str) -> Optional[bytes]:
    db_key = _generate_db_key(job_id=str(job_id).encode(), size=size)
    img_encoded = db.redis_conn.get(db_key)
    if not img_encoded:
        return None
    img = base64.b64decode(img_encoded)
    return img


def save_file_to_db(key: bytes, file: bytes) -> None:
    db.redis_conn.set(key, base64.b64encode(file))


def get_task_status(job_id: int) -> Optional[Status]:
    try:
        job = Job.fetch(str(job_id), connection=db.redis_conn)
    except NoSuchJobError:
        return None

    status = job.get_status()

    if status == JobStatus.FAILED:
        return Status.failed
    if status == JobStatus.STARTED:
        return Status.in_progress
    if status == JobStatus.FINISHED:
        return Status.done

    return Status.waiting


def create_task(file: bytes) -> int:
    job_id = _get_id_for_new_job()

    db_original_img_key = _generate_db_key(job_id=job_id, size='original')
    save_file_to_db(key=db_original_img_key, file=file)

    db.queue.enqueue(
        _resize_images_and_save_to_db, job_id, file, job_id=job_id.decode()
    )

    return int(job_id)


def _generate_db_key(job_id: bytes, size: str) -> bytes:
    return job_id + f'-{size}'.encode()


def _get_id_for_new_job() -> bytes:
    with db.redis_conn.lock('counter_lock'):
        counter = db.redis_conn.get('counter')
        if not counter:
            counter = b'1'
            db.redis_conn.set('counter', counter)

        db.redis_conn.incr('counter')
        return counter


def _resize_image(file: bytes, size: int) -> bytes:
    image = Image.open(BytesIO(file))
    resized_image = image.resize((size, size))
    image_bytes = BytesIO()
    resized_image.save(image_bytes, format='PNG')
    image_bytes.seek(0)
    return image_bytes.getvalue()


def _resize_images_and_save_to_db(job_id: bytes, file: bytes) -> None:
    for size in (32, 64):
        bytes_img = _resize_image(file, size)
        db_key = _generate_db_key(job_id=job_id, size=str(size))
        save_file_to_db(key=db_key, file=bytes_img)
