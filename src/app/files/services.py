from datetime import datetime
from typing import List

from fastapi import UploadFile

from src.app.base.utils.email_sender import get_admin_email_list
from src.app.files.models import File, StatusFileEnum
from src.app.worker import send_email_task
from src.app.users.models import User


async def send_message_files_add(current_user: User, files: UploadFile | List[UploadFile]):
    """
    Отправка сообщение администраторам сервиса о загрузке нового файла (файлов)

    :param current_user: Пользователь загрузивший файл
    :param files: добавленный файл - UploadFile (файлы - List[UploadFile])
    """
    time_now = f"{datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC"

    file_list = files if isinstance(files, list) else [files]
    filename_list = [file.filename for file in file_list]

    subject = f'Новые документы на проверку'
    environment = {
                'user_email': current_user.email,
                'files': filename_list,
                'time_upload': time_now
            }

    send_email_task.delay(
        email_to=await get_admin_email_list(),
        subject=subject,
        template_name='files_add.html',
        environment=environment
    )


async def send_message_file_status(file: File):
    """
    Отправка сообщения пользователю об изменении статуса проверки его файла

    :param file: Файл с измененным статусом
    """
    time_now = f"{datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC"

    user = await file.owner
    user_name = f'{user.first_name} {user.surname}'

    match file.status:
        case StatusFileEnum.ACCEPTED:
            file_status = "ПРИНЯТ"
        case StatusFileEnum.REJECTED:
            file_status = "ОТКЛОНЕН"
        case _:
            file_status = "На рассмотрении"

    subject = f'Результат проверки документа'
    environment = {
                'user_name': user_name,
                'file': file.name,
                'status': file_status,
                'time_update': time_now
            }

    send_email_task.delay(
        email_to=user.email,
        subject=subject,
        template_name='file_status.html',
        environment=environment
    )
