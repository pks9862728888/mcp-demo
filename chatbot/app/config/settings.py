from pydantic_settings import BaseSettings
import os
from dotenv import load_dotenv


class Settings(BaseSettings):
    profile: str
    log_level: str


env_profile = os.environ.get("ACTIVE_PROFILE")
if env_profile is None:
    raise ValueError("ACTIVE_PROFILE is not set")
load_dotenv(f".env.{env_profile.lower()}")

settings = Settings()  # type: ignore
