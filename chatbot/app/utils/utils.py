from app.config.settings import settings
from app.config.logger import logger


def print_env() -> None:
    logger.info(f"Profile: {settings.profile}")
