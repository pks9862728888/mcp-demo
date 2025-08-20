from langchain_core.prompts import PromptTemplate, \
ChatPromptTemplate, MessagesPlaceholder, FewShotPromptTemplate
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


def few_shot_prompt_template():
    """
    Used to create a few-shot prompt with multiple examples
    """
    example_prompt = PromptTemplate.from_template("Question: {question}\n{answer}")
    examples = get_example_set()
    # print(example_prompt.invoke(examples[0]).to_string())
    prompt = FewShotPromptTemplate(
        examples = examples,
        example_prompt = example_prompt,
        suffix = "Question: {input}",
        input_variables = ["input"]
    )
    formatted_prompt = prompt.invoke({"input": "Who is the father of computer?"})
    print(formatted_prompt.to_string())
    chat_with_model(formatted_prompt)


def get_example_set() -> list[dict]:
    return [
        {
            "question": "Who lived longer, Muhammad Ali or Alan Turing?",
            "answer": """
Are follow up questions needed here: Yes.
Follow up: How old was Muhammad Ali when he died?
Intermediate answer: Muhammad Ali was 74 years old when he died.
Follow up: How old was Alan Turing when he died?
Intermediate answer: Alan Turing was 41 years old when he died.
So the final answer is: Muhammad Ali
""",
        },
        {
            "question": "When was the founder of craigslist born?",
            "answer": """
Are follow up questions needed here: Yes.
Follow up: Who was the founder of craigslist?
Intermediate answer: Craigslist was founded by Craig Newmark.
Follow up: When was Craig Newmark born?
Intermediate answer: Craig Newmark was born on December 6, 1952.
So the final answer is: December 6, 1952
""",
        }
    ]