from tortoise import models, fields


class User(models.Model):
    """ Модель пользователя """
    id = fields.IntField(pk=True, description='Идентификатор')
    username = fields.CharField(max_length=150, null=True, default=None, description='Имя пользователя')
    email = fields.CharField(max_length=255, unique=True, description='Адрес электронной почты')
    password = fields.CharField(max_length=100, description='Пароль')
    last_name = fields.CharField(max_length=30, description='Фамилия')
    first_name = fields.CharField(max_length=30, description='Имя')
    surname = fields.CharField(max_length=30, null=True, description='Отчество')
    date_joined = fields.DatetimeField(auto_now_add=True, description='Дата регистрации')
    last_login = fields.DatetimeField(null=True, description='Дата последнего входа')
    is_active = fields.BooleanField(default=True, description='Признак активности')
    is_staff = fields.BooleanField(default=False, description='Признак персонала')
    is_superuser = fields.BooleanField(default=False, description='Признак администратора')
    comments = fields.TextField(null=True, description='Информация о пользователе')

    class PydanticMeta:
        exclude = ['password']
