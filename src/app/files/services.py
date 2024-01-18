from datetime import datetime
from typing import Any

from src.app.base.utils.email_sender import get_admin_email_list
from src.app.worker import send_email_task
from src.app.users.models import User


async def send_message_add_files(current_user: User, files: Any):
    """
    Отправка сообщение администраторам сервиса о загрузке нового файла (файлов)

    :param current_user: Пользователь загрузивший файл
    :param files: добавленный файл - UploadFile (файлы - List[UploadFile])
    """
    time_now = f"{datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC"

    file_list = files if isinstance(files, list) else [files]
    file_name_list = [file.filename for file in file_list]

    subject = f'Новые документы на проверку'
    environment = {
                'user_email': current_user.email,
                'files': file_name_list,
                'time_upload': time_now
            }

    send_email_task.delay(
        email_to=await get_admin_email_list(),
        subject=subject,
        template_name='file_add.html',
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
