import os
from app.config.logger import logger

def validate_open_ai_key_exists() -> None:
  if not os.getenv('OPENAI_API_KEY'):
    raise ValueError("Missing OPENAI_API_KEY")
  else:
    logger.info("OPENAI_API_KEY is set")

