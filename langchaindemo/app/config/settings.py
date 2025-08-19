
from pydantic import BaseModel
from dotenv import load_dotenv
import os

from pydantic_settings import BaseSettings

load_dotenv();

class Settings(BaseSettings):
    openai_api_key: str

settings = Settings() # type: ignore
