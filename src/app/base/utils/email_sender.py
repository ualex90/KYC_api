import emails
from emails.template import JinjaTemplate

from src.config import settings

password_reset_jwt_subject = "preset"


def send_email(
        email_to: str,
        subject_template: str = "",
        html_template: str = "",
        environment: dict = None
):
    """
    Отправка email


    """
    assert settings.EMAILS_ENABLED, "no provided configuration for email variables"
    message = emails.Message(
        subject=JinjaTemplate(subject_template),
        html=JinjaTemplate(html_template),
        mail_from=('KYC Service', settings.EMAIL_USER),
    )
    smtp_options = {
        "host": settings.EMAIL_HOST,
        "port": settings.EMAIL_PORT,
        "user": settings.EMAIL_USER,
        "password": settings.EMAIL_PASSWORD,
        "tls": settings.EMAIL_USE_TLS,
    }
    print(smtp_options)
    response = message.send(to=email_to, render=environment, smtp=smtp_options)
    print(f"send email result: {response}")


def send_test_email(email_to: str):
    """
    Отправка тестового письма


    """
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - Test email"
    with open(settings.EMAIL_TEMPLATES_DIR / "test_email.html") as f:
        template_str = f.read()
    send_email(
        email_to=email_to,
        subject_template=subject,
        html_template=template_str,
        environment={"project_name": settings.PROJECT_NAME, "email": email_to},
    )


if __name__ == "__main__":
    send_test_email(
        email_to="u_alex90@mail.ru",
    )
