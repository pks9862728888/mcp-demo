from dotenv import load_dotenv
import os

from openai import OpenAI

load_dotenv()


def get_openai_api_key():
    """
    This function returns open api key from environement variable
    """
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        raise ValueError("OPENAI_API_KEY is not set")
    return openai_api_key


openai_client = OpenAI(api_key=get_openai_api_key())
