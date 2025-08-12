import uuid
from PIL import Image

from fastapi import UploadFile
from pydantic import field_validator, BaseModel

from rest.schemas.form import BaseForm


class NovelForm(BaseForm):
    title: str
    img: UploadFile | None

    @field_validator("img")
    @classmethod
    def validate_img(cls, v):
        if not v:
            return v
        if v.size > 10 * 1024 * 1024:
            raise ValueError("Размер изображение не должен превышать 10МБ.")
        try:
            img = Image.open(v.file)
            img.verify()
        except OSError:
            raise ValueError("Изображение повреждено.")
        return v


class NovelToDB(BaseModel):
    title: str
    obj_cover_name: uuid.UUID
