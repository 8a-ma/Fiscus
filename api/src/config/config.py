import os
import logging
from pathlib import Path
from dotenv import load_dotenv


def _resolve_log_level(level_name: str) -> int:
    """Return a valid logging level; default to INFO for unknown values."""
    if not level_name:
        return logging.INFO
    level_name = level_name.upper()
    return getattr(logging, level_name, logging.INFO)


ROOT_ENV = Path(__file__).resolve().parents[2] / ".env"
if ROOT_ENV.exists():
    load_dotenv(dotenv_path=ROOT_ENV)
else:
    load_dotenv()


class Config:
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

    POSTGRESQL_POOL_MIN = 1
    POSTGRESQL_POOL_MAX = 4

    POSTGRES_HOST = os.getenv("POSTGRES_HOST")
    POSTGRES_DB = os.getenv("POSTGRES_DB")
    POSTGRES_USER = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_PORT = os.getenv("POSTGRES_PORT")
    POSTGERSQL_QUERY_TIMEOUT = 10

    # src path
    ROOT_PATH = Path(__file__).resolve().parents[1]

    API_KEY = os.getenv("API_KEY")

    @classmethod
    def get_logger(cls, name: str) -> logging.Logger:
        level = _resolve_log_level(cls.LOG_LEVEL)
        root_logger = logging.getLogger()
        format = "%(asctime)s %(levelname)s [%(name)s, %(funcName)s] %(message)s"

        if not root_logger.handlers:
            logging.basicConfig(
                level=level,
                format=format
            )
        else:
            root_logger.setLevel(level)
            root_logger.setFormatter(format)

            for handler in root_logger.handlers:
                handler.setLevel(level)
                handler.setFormatter(format)

            logger = logging.getLogger(name)
            logger.setLevel(level)
            logger.setFormatter(format)

            return logger
