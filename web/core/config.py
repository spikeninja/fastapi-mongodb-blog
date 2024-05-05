import os
from pydantic import computed_field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    secret_key: str = os.getenv('SECRET_KEY')

    # SMTP CONFIGS
    smtp_email: str = os.getenv('SMTP_EMAIL')
    smtp_server: str = os.getenv("SMTP_SERVER")
    smtp_password: str = os.getenv('SMTP_PASSWORD')
    smtp_port: str = os.getenv("SMTP_PORT", default=465)

    # MONGODB
    mongodb_database: str = os.getenv("MONGO_INITDB_DATABASE")
    mongodb_user: str = os.getenv("MONGO_INITDB_ROOT_USERNAME")
    mongodb_password: str = os.getenv("MONGO_INITDB_ROOT_PASSWORD")

    @computed_field
    @property
    def mongodb_url(self) -> str:
        return f"mongodb://{self.mongodb_user}:{self.mongodb_password}@mongodb:27017/{self.mongodb_database}"

    # LOGGING
    logger_level: str = os.getenv("LOGGER_LEVEL")
    logger_filename: str = os.getenv("LOGGER_FILENAME")

    # CELERY
    celery_broker_url: str = os.getenv("BROKER_URL")
    celery_backend_url: str = os.getenv("BACKEND_URL")

    # TWO_FA REDIS URL
    two_fa_redis: str = os.getenv("TWO_FA_REDIS")
    two_fa_enabled: bool = os.getenv("TWO_FA_ENABLED") in {'t', 'true', '1'}
    two_fa_repeat_days: int = os.getenv("TWO_FA_REPEAT_DAYS")
    two_fa_code_lifetime: int = os.getenv("TWO_FA_CODE_LIFETIME")

    # FILES PROPERTIES
    max_file_size: int = 10 * 1024 * 1024

    # CREDITS
    generation_price: int = 10


settings = Settings()
