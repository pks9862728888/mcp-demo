from langchain_core.prompts import PromptTemplate, ChatPromptTemplate, MessagesPlaceholder
from app.model import model


def chat_with_model(prompt):
    print(prompt)
    response = model.invoke(prompt)
    print(response.content)


def string_prompt_template(topic):
    """
    Used to format a single string
    """
    prompt_template = PromptTemplate.from_template("Tell me a joke about {topic}")
    formatted_prompt = prompt_template.invoke({"topic": topic})
    chat_with_model(formatted_prompt)


def chat_prompt_template(topic):
    """
    Used to pass two messages when called, system message and human message
    """
    prompt_template = ChatPromptTemplate([
        ("system", "You are a person who can crack decent tech jokes"),
        ("user", f"Tell me a joke about {topic}")
    ])
    formatted_prompt = prompt_template.format_messages(topic=topic)
    chat_with_model(formatted_prompt)


def messages_placeholder(messages_to_pass):
    """
    Used to pass a list of conversation history to the model
    """
    prompt_template = ChatPromptTemplate([
        ("system", "You are a tech joke teller assistant who speak like a pirate"),
        MessagesPlaceholder("msgs")
    ])
    formatted_prompt = prompt_template.invoke({
        "msgs": messages_to_pass
    })
    chat_with_model(formatted_prompt)

