from app.config import settings
from app.prompt_templates import chat_prompt_template, chat_with_model, few_shot_chat_message_prompt_template, few_shot_prompt_template, messages_placeholder, string_prompt_template
from langchain_core.messages import HumanMessage, AIMessage

from app.structured_outputs import structured_output_tool_calls, structured_output_json_mode


def prompt_templates():
    # string_prompt_template("computer")
    # chat_prompt_template("computer")
    # messages_placeholder([
    #     HumanMessage("What's your favorite programming language?"),
    #     AIMessage("Ayey mate, mine is Python!"),
    #     HumanMessage("So tell me something pythony??")
    # ])
    # few_shot_prompt_template()
    # few_shot_chat_message_prompt_template()
    pass


def structured_output():
    # structured_output_tool_calls("How should I learn AI?")
    structured_output_json_mode("How much time is required to learn AI?")


def main():
    pass


if __name__ == "__main__":
    main()
