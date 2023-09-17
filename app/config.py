from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Database Environment Variables
    DATABASE_HOSTNAME: str
    DATABASE_PORT: str
    DATABASE_PASSWORD: str
    DATABASE_NAME: str
    DATABASE_USERNAME: str

    # JWT Token Environment Variables
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    class Config:
        env_file = ".env"


settings = Settings()

print(settings.DATABASE_USERNAME)
