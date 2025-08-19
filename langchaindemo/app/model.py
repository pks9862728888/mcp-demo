from langchain.chat_models import init_chat_model

model = init_chat_model("gpt-4o-mini", model_provider="openai")

def chat_with_model(prompt):
    print(prompt)
    value = model.invoke(prompt)
    print(value)

