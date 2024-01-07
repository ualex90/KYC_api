from tortoise import models, fields
from src.app.users.models import User


class File(models.Model):
    id = fields.IntField(pk=True)
    owner: fields.ForeignKeyRelation['User'] = fields.ForeignKeyField(
        'models.User', related_name='files', on_delete=fields.CASCADE
    )
    file = fields.CharField(max_length=300, unique=True)
    # status =
