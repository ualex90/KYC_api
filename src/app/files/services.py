from fastapi import UploadFile

from src.app.base.utils.email_sender import get_admin_email_list
from src.app.worker import send_email_task
from src.app.users.models import User


async def send_message_add_files(current_user: User, files: list[UploadFile]):
    """
    Отправка сообщение администраторам сервиса о загрузке нового файла

    :param current_user: Пользователь загрузивший файл
    :param files: добавленные файлы
    """
    subject = f'Загружены документы на проверку'
    environment = {
                "project_name": files[0].filename,
                "email": current_user.email,
            }

    send_email_task.delay(
        email_to=await get_admin_email_list(),
        subject=subject,
        template_name='email_test.html',
        environment=environment
    )


if __name__ == '__main__':
    send_email_task.delay(
        email_to=['u_alex90@mail.ru', 'admin@sky.pro'],
        # email_to='u_alex90@mail.ru',
        subject='Загружены документы от на проверку',
        template_name='email_test.html',
        environment={
                "project_name": 'DSC07491.JPG',
                "email": 'ivanov@sky.pro',
            }
    )
