from enum import Enum

from tortoise import models, fields
from src.app.users.models import User


class StatusFileEnum(str, Enum):
    UNDER_REVIEW = 'under_review'
    ACCEPTED = 'accepted'
    REJECTED = 'rejected'


class File(models.Model):
    id = fields.IntField(pk=True, description='Идентификатор')
    file_name = fields.CharField(max_length=50, description='Имя файла')
    owner: fields.ForeignKeyRelation['User'] = fields.ForeignKeyField(
        'models.User',
        related_name='files',
        on_delete=fields.CASCADE,
        null=True,
        description='Владелец'
    )
    path = fields.CharField(max_length=30, unique=True, description='Имя файла на диске')
    status = fields.CharEnumField(
        enum_type=StatusFileEnum,
        default=StatusFileEnum.UNDER_REVIEW,
        description='Статус файла'
    )
