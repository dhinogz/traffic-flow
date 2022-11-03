from pathlib import Path
from sys import modules

from pydantic import BaseSettings


BASE_DIR = Path(__file__).parent.resolve()


class Settings(BaseSettings):
    """Application settings."""

    ENV: str = "dev"
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    BASE_URL_: str = f"https://{HOST}:{PORT}/"
    # quantity of workers for uvicorn
    WORKERS_COUNT: int = 1
    # Enable uvicorn reloading
    RELOAD: bool = True

    class Config:
        env_file = f"{BASE_DIR}/.env"
        env_file_encoding = "utf-8"
        fields = {
            "BASE_URL_": {
                "env": "BASE_URL",
            },
        }


settings = Settings()

if "pytest" in modules:
    settings.DB_BASE += "_test"
