from openai import OpenAI
import os

from utils import openai_client


def print_response_from_openai_client():
    # print(f"key: {openai_client.api_key}")
    response = openai_client.chat.completions.create(
        model="gpt-4.1",
        messages=[
            {"role": "developer", "content": "Talk like a pirate."},
            {"role": "user", "content": "Write a line about python."},
        ],
    )
    print(response)
    print(response.choices[0].message.content)


def main():
    print_response_from_openai_client()


if __name__ == "__main__":
    main()
