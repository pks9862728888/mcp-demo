from app.config import settings
from app.model import chat_with_model


def main():
    chat_with_model("Hello, how can I assist you today?")


if __name__ == "__main__":
    main()
