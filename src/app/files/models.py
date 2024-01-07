from enum import Enum

from tortoise import models, fields
from src.app.users.models import User


class StatusFileEnum(str, Enum):
    UNDER_REVIEW = 'under_review'
    ACCEPTED = 'accepted'
    REJECTED = 'rejected'


class File(models.Model):
    id = fields.IntField(pk=True, description='Идентификатор')
    name = fields.CharField(max_length=50, description='Имя файла')
    size = fields.IntField(description='Размер файла')
    content_type = fields.CharField(max_length=30, description='Тип файла')
    filename = fields.CharField(max_length=30, unique=True, description='Имя файла на диске')
    status = fields.CharEnumField(
        enum_type=StatusFileEnum,
        default=StatusFileEnum.UNDER_REVIEW,
        description='Статус файла'
    )
    owner: fields.ForeignKeyRelation['User'] = fields.ForeignKeyField(
        'models.User',
        related_name='files',
        on_delete=fields.SET_NULL,
        null=True,
        description='Владелец'
    )
    upload_at = fields.DatetimeField(auto_now_add=True, description='Дата и время загрузки файла')
