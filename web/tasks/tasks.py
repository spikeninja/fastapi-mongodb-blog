import time
import random
import asyncio
from uuid import uuid4
from io import BytesIO
from hashlib import md5
from datetime import datetime
from mimetypes import guess_type

from PIL import Image
from celery import Celery

from core.config import settings
from db.files import MinioProvider
from ext.functions import send_email
from services.files import FilesService
from db.database import DatabaseProvider
from repository.files import FileRepository
from repository.generations import GenerationsRepository


worker = Celery(broker=settings.celery_broker_url, backend=settings.celery_backend_url)


@worker.task
def task_send_email(recipients: list[str], subject: str, body: str):
    """"""

    send_email(recipients=recipients, subject=subject, body=body)


async def save_generation_results(
    user_id: str,
    generation_id,
    generated_name: str,
    generated_bytes: bytes,
):
    """"""

    file_repo = FileRepository(database=DatabaseProvider())
    generation_repo = GenerationsRepository(database=DatabaseProvider())

    await file_repo.create(
        size=len(generated_bytes),
        file_url=generated_name,
        old_name=generated_name,
        user_id=user_id,
        content_type=guess_type(generated_name)[0],
        _hash=md5(generated_bytes).hexdigest(),
        file_name=generated_name,
    )

    now_ = datetime.utcnow()
    await generation_repo.update(
        _id=generation_id,
        values={
            "state": "done",
            "generated_at": now_,
            "result_name": generated_name,
        }
    )


@worker.task
def task_generate_photo(
    user_id: str,
    mask_name: str,
    reference_name: str,
    generation_id: str,
):
    """"""
    file_service = FilesService(
        minio_client=MinioProvider(),
        bucket_name=settings.bucket_name,
    )

    # Getting files from Storage
    # mask_bytes = file_service.sync_get_file(file_name=mask_name)
    reference_bytes = file_service.sync_get_file(file_name=reference_name)

    # 1. send to image generation service
    # mask = Image.open(BytesIO(mask_bytes))
    reference = Image.open(BytesIO(reference_bytes))

    # 2. got generated image
    buf = BytesIO()
    generated = reference.convert('L')
    generated.save(buf, format="JPEG")
    buf.seek(0)

    # some sleep...
    time.sleep(random.randint(15, 30))

    # 3. create that image using FileRepo (set current user_id)
    generated_ext = reference_name.split(".")[1]
    generated_name = f"{uuid4()}.{generated_ext}"

    file_service.sync_put_file(content=buf.getvalue(), file_name=generated_name)

    # 4. Update Generation and Files Repo with new generated image id
    asyncio.run(
        save_generation_results(
            user_id=user_id,
            generation_id=generation_id,
            generated_name=generated_name,
            generated_bytes=buf.getvalue(),
        )
    )
