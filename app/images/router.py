import os
import shutil

from fastapi import APIRouter, UploadFile

from app.tasks.tasks import process_pic

router = APIRouter(prefix="/images", tags=["Загрузка картинок"])


@router.post("/hotels")
async def add_hotel_image(name: int, file: UploadFile):
    filename, file_extension = os.path.splitext(file.filename)
    im_path = f"app/static/images/{name}{file_extension}"
    with open(im_path, "wb+") as file_object:
        shutil.copyfileobj(file.file, file_object)
    process_pic.delay(im_path)
