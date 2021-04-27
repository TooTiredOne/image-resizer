from enum import Enum
from typing import Optional

from fastapi import APIRouter, File, HTTPException, Query, UploadFile
from fastapi.responses import Response

from app import crud
from app.validators import check_if_file_is_image, check_if_image_is_square

router = APIRouter()


class ImageSize(str, Enum):
    size_original = 'original'
    size_32 = '32'
    size_64 = '64'


@router.post('', status_code=201)
def create_task(file: UploadFile = File(...)) -> Optional[int]:
    file_bytes = file.file.read()
    if not check_if_file_is_image(file_bytes):
        raise HTTPException(status_code=422, detail='File must be image')
    if not check_if_image_is_square(file_bytes):
        raise HTTPException(status_code=422, detail='Image must be square')
    return crud.create_task(file_bytes)


@router.get('/{job_id}', status_code=200)
def get_task_status(job_id: int = Query(..., gt=0)) -> Optional[str]:
    status = crud.get_task_status(job_id)
    if not status:
        raise HTTPException(status_code=404, detail='Task not found')
    return status.value


@router.get('/{job_id}/image', status_code=200)
def get_image(
    job_id: int = Query(..., gt=0),
    size: ImageSize = ImageSize.size_original,
) -> Optional[Response]:
    image = crud.get_image_from_db(job_id=job_id, size=size.value)
    if not image:
        raise HTTPException(status_code=404, detail='Image not found')
    return Response(image, media_type='image/png')
