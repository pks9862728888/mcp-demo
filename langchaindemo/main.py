from app.config import settings
from app.prompt_templates import chat_prompt_template, chat_with_model, few_shot_chat_message_prompt_template, few_shot_prompt_template, messages_placeholder, string_prompt_template
from langchain_core.messages import HumanMessage, AIMessage

def main():
    # string_prompt_template("computer")
    # chat_prompt_template("computer")
    # messages_placeholder([
    #     HumanMessage("What's your favorite programming language?"),
    #     AIMessage("Ayey mate, mine is Python!"),
    #     HumanMessage("So tell me something pythony??")
    # ])
    # few_shot_prompt_template()
    few_shot_chat_message_prompt_template()


if __name__ == "__main__":
    main()
