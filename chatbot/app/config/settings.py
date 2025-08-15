from pydantic_settings import BaseSettings
import os
from dotenv import load_dotenv


class Settings(BaseSettings):
    profile: str
    log_level: str
    CHAT_MODEL: str = "openai:gpt-4.1"
    LANGCHAIN_API_KEY: str
    LANGCHAIN_TRACING_V2: str
    OPENAI_API_KEY: str


def get_active_profile() -> str:
    env_profile = os.environ.get("ACTIVE_PROFILE")
    if env_profile is None:
        raise ValueError("ACTIVE_PROFILE is not set")
    return env_profile


def load_env() -> None:
    load_dotenv(f".env.{get_active_profile().lower()}")


load_env()
settings = Settings()  # type: ignore
