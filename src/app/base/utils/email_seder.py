import smtplib
from email.mime.text import MIMEText

import jinja2

from src.config import settings


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
        email_to: str,
        subject: str,
        template_name: str,
        environment: dict = None,
):
    """
    Отправка сообщения

    Отправляет сообщение основанное на "template_name" с переменными "environment"
    получателю "email_to" на тему "subject"

    :param email_to: Email получателя
    :param subject: Тема сообщения
    :param template_name: Имя jinja шаблона (из папки шаблонов определенной по пути settings.TEMPLATES_DIR)
    :param environment: Переменные для сборки шаблона
    :return:
    """
    assert settings.EMAILS_ENABLED, "no provided configuration for email variables"
    sender = f'{settings.PROJECT_NAME} <{settings.EMAIL_USER}>'
    server = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
    if settings.EMAIL_USE_TLS:
        server.starttls()

    try:
        server.login("noreply-90@yandex.ru", settings.EMAIL_PASSWORD)
        template = render_template(template_name=template_name, **environment)
        msg = MIMEText(template, "html")
        msg["From"] = sender
        msg["To"] = email_to
        msg["Subject"] = subject
        server.sendmail(sender, email_to, msg.as_string())
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
