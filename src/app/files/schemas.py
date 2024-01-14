from pydantic import BaseModel


class FileBaseSchema(BaseModel):
    """ Базовая модель пользователя """
    filename: str
    name: str
    status: str
    owner: int

    class Config:
        json_schema_extra = {
            "example": {
                "filename": "ID",
                "name": "Имя",
                "status": "Имя файла в хранилище",
                "owner": "ID владельца"
            }
        }

