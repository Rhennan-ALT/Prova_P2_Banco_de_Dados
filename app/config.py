from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    MONGO_URL: str
    RABBITMQ_HOST: str
    KAFKA_BOOTSTRAP: str

    class Config:
        env_file = ".env"

settings = Settings()