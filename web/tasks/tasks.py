from celery import Celery

from core.config import settings
from ext.functions import send_email


worker = Celery(broker=settings.celery_broker_url, backend=settings.celery_backend_url)


@worker.task
def task_send_email(recipients: list[str], subject: str, body: str):
    """"""

    send_email(recipients=recipients, subject=subject, body=body)
