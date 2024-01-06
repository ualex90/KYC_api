from tortoise import models, fields


class User(models.Model):
    """ Модель пользователя """
    id = fields.IntField(pk=True, description='Идентификатор')
    email = fields.CharField(max_length=255, unique=True, description='Адрес электронной почты')
    password = fields.CharField(max_length=100, description='Пароль')
    last_name = fields.CharField(max_length=30, description='Фамилия')
    first_name = fields.CharField(max_length=30, description='Имя')
    surname = fields.CharField(max_length=30, null=True, description='Отчество')
    join_date = fields.DatetimeField(auto_now_add=True, description='Дата регистрации')
    is_active = fields.BooleanField(default=True, description='Признак активности')
    is_staff = fields.BooleanField(default=False, description='Признак персонала')
    is_superuser = fields.BooleanField(default=False, description='Признак администратора')
    comments = fields.TextField(null=True, description='Информация о пользователе')

    def __str__(self):
        return self.email

    class PydanticMeta:
        exclude = ['password']