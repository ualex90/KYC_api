import emails
from emails.template import JinjaTemplate

from src.config import settings


def send_email(
        email_to: str,
        subject: str,
        template_name: str,
        environment: dict = None
):
    """
    Отправка сообщения

    Отправляет сообщение основанное на "template_name" с переменными "environment"
    получателю "email_to" на тему "subject"

    :param email_to: Email получателя
    :param subject: Тема сообщения
    :param template_name: Имя jinja шаблона (из папки шаблонов определенной по пути settings.TEMPLATES_DIR)
    :param environment: Переменные для сборки шаблона
    :return: Результат попытки отправки сообщения
    """
    assert settings.EMAILS_ENABLED, "no provided configuration for email variables"
    try:
        with open(settings.TEMPLATES_DIR / template_name) as f:
            template = f.read()
    except IOError:
        f'Template file not found: {settings.TEMPLATES_DIR / template_name}'
    message = emails.Message(
        subject=subject,
        html=JinjaTemplate(template),
        mail_from=(settings.PROJECT_NAME, settings.EMAIL_USER),
    )
    smtp_options = {
        "host": settings.EMAIL_HOST,
        "port": settings.EMAIL_PORT,
        "user": settings.EMAIL_USER,
        "password": settings.EMAIL_PASSWORD,
        "tls": settings.EMAIL_USE_TLS,
    }
    response = message.send(to=email_to, render=environment, smtp=smtp_options)
    return f"send email result: {response}"


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


if __name__ == "__main__":
    send_test_email("u_alex90@mail.ru")
