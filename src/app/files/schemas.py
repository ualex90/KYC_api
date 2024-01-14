from datetime import datetime

from pydantic import BaseModel

from src.app.files.models import StatusFileEnum


class FileBaseSchema(BaseModel):
    """ Базовая схема файла """
    id: int
    name: str
    status: StatusFileEnum
    owner: str
    is_public: bool

    class Config:
        json_schema_extra = {
            "example": {
                "ID": "Идентификатор",
                "name": "Имя",
                "status": "Статус проверки файла",
                "owner": "Email владельца",
                "is_public": "Признак публичности",
            }
        }


class FileSchema(FileBaseSchema):
    """ Полная модель файла """
    filename: str
    size: float
    content_type: str
    upload_at: datetime

    class Config:
        json_schema_extra = {
            "example": {
                "ID": "Идентификатор",
                "name": "Имя",
                "status": "Статус проверки файла",
                "owner": "Email владельца",
                "is_public": "Признак публичности",
                "filename": "Имя файла в хранилище",
                "size": "Размер файла байт",
                "content_type": "Тип файла",
                "upload_at": "Дата загрузки",
            }
        }
