from app.config import settings
from app.prompt_templates import chat_prompt_template, chat_with_model, messages_placeholder, string_prompt_template
from langchain_core.messages import HumanMessage, AIMessage

def main():
    # string_prompt_template("computer")
    # chat_prompt_template("computer")
    messages_placeholder([
        HumanMessage("What's your favorite programming language?"),
        AIMessage("Ayey mate, mine is Python!"),
        HumanMessage("So tell me something pythony??")
    ])


if __name__ == "__main__":
    main()
