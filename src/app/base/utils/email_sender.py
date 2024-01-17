import smtplib
from email.mime.text import MIMEText
from typing import Any

import jinja2

from src.app.users.models import User
from src.config import settings


async def get_admin_email_list() -> list[str]:
    """
    Получение списка email адресов администраторов системы
    """
    admin_query = await User.all().filter(is_superuser=True)
    email_list = [i.email for i in admin_query]
    return email_list


def render_template(template_name: str, **kwargs) -> str:
    """
    Сборка Jinja шаблона в готовый html документ

    :param template_name: имя шаблона в формате "template.html"
    :param kwargs: переменные для сборки шаблона
    :return: html документ
    """
    # Определение каталога шаблонов по умолчанию
    templateLoader = jinja2.FileSystemLoader(searchpath=settings.TEMPLATES_DIR)
    templateEnv = jinja2.Environment(loader=templateLoader)

    # Проверка существования шаблона
    try:
        template = templateEnv.get_template(template_name)
    except jinja2.TemplateNotFound as error:
        error.message = f'Template file not found: {settings.TEMPLATES_DIR / template_name}'
        raise error
    # В случае успеха, возвращаем собранный html документ
    return template.render(**kwargs)


def send_email(
        email_to: Any,
        subject: str,
        template_name: str,
        environment: dict = None,
):
    """
    Отправка сообщения

    Отправляет сообщение основанное на "template_name" с переменными "environment"
    получателю "email_to" на тему "subject"

    :param email_to: Email получателя - str (получателей - list)
    :param subject: Тема сообщения
    :param template_name: Имя jinja шаблона (из папки шаблонов определенной по пути settings.TEMPLATES_DIR)
    :param environment: Переменные для сборки шаблона
    :return: Результат попытки отправки сообщения
    """
    # Проверка заполнения переменных окружения для почты
    assert settings.EMAILS_ENABLED, "no provided configuration for email variables"

    # Преобразование значения email_to в list если оно str
    email_to_list = list(email_to) if isinstance(email_to, str) else email_to

    # Составление строки отправителя
    email_from = f'{settings.PROJECT_NAME} <{settings.EMAIL_USER}>'

    # Сборка шаблона
    template = render_template(template_name=template_name, **environment)

    # Подключение к серверу SMTP и отправка сообщения
    server = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
    if settings.EMAIL_USE_TLS:
        server.starttls()
    try:
        server.login(settings.EMAIL_USER, settings.EMAIL_PASSWORD)

        # From и To необходимо определить для предотвращения блокировки спам фильтром яндекс
        msg = MIMEText(template, "html")
        msg["From"] = email_from
        msg["To"] = ', '.join(email_to_list)
        msg["Subject"] = subject

        server.sendmail(email_from, email_to_list, msg.as_string())
        return f'The message "{subject}" to "{email_to}" was sent successfully!'
    except (
            smtplib.SMTPAuthenticationError,
            smtplib.SMTPSenderRefused
    ) as error:
        return f'{error.args}'


def send_test_email(email_to: str):
    """
    Отправка тестового письма
    """
    send_email(
        email_to=email_to,
        subject="Тестовое сообщение",
        template_name='email_test.html',
        environment={
            "project_name": settings.PROJECT_NAME,
            "email": email_to,
        }
    )


if __name__ == '__main__':
    send_test_email("u_alex90@mail.ru")
