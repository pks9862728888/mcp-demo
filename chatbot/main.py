import asyncio

from app.config import settings  # noqa: F401
from app.config import logger  # noqa: F401
from app.openai import validate_open_ai_key_exists
from app.utils import utils


async def validate_env() -> None:
    utils.print_env()
    validate_open_ai_key_exists()


async def main():
    await validate_env()


if __name__ == "__main__":
    asyncio.run(main())
