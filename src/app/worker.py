from celery import Celery

from src.app.base.utils.email_sender_old import send_email
from src.config import settings


app = Celery(
    main=__name__,
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND
)


@app.task
def send_email_task(**kwargs):
    response = send_email(**kwargs)
    return response
