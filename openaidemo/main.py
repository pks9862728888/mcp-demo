from dotenv import load_dotenv
from openai import OpenAI
import os

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise ValueError("OPENAI_API_KEY is not set")
openai_client = OpenAI(api_key=openai_api_key)

def print_response_from_openai_client():
    print(openai_client.api_key[0:10])
    response = openai_client.chat.completions.create(
        model="gpt-4o",
        messages = [
            {"role": "developer", "content": "Talk like a pirate."},
            {"role": "user", "content": "Write a one-sentence bedtime story about a unicorn."}
        ]
    )
    print(response.choices[0].message.content)

def main():
    print_response_from_openai_client()
    

if __name__ == "__main__":
    main()
