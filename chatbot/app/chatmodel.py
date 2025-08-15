import os
from langchain.chat_models import init_chat_model
from langgraph.graph import START, END

from app.config.logger import logger
from app.config.settings import settings
from app.stategraph import State, graph_builder


llm = init_chat_model(settings.CHAT_MODEL, verbose=True)


def chatbot(state: State):
    return {"messages": [llm.invoke(state["messages"])]}


# The first argument is the unique node name
# The second argument is the function or object that will be called whenever
# the node is used.
graph_builder.add_node("chatbot", chatbot)
# tell the graph where to start its work
graph_builder.add_edge(START, "chatbot")
# tell the graph where to end its work
graph_builder.add_edge("chatbot", END)


def build_and_display_graph():
    """Builds the state graph and displays it."""
    logger.info("Building and displaying the state graph...")
    global graph
    graph = graph_builder.compile()
    try:
        output_path = os.path.join("out", "my_graph.png")
        with open(output_path, "wb") as f:
            f.write(graph.get_graph().draw_mermaid_png())
        os.startfile(output_path)
    except Exception as e:
        logger.error(f"Error displaying graph: {e}")


def stream_graph_updates(user_input: str) -> None:
    for event in graph.stream({
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_input}
        ]
    }):
        for value in event.values():
            print(f"Assistant: {value['messages'][-1].content}\n")


def start_chatbot() -> None:
    """Starts the chatbot interaction."""
    logger.info("Starting chatbot interaction...")
    user_input = input("User: ")
    while user_input.lower() not in ["exit", "quit", "q"]:
        stream_graph_updates(user_input)
        user_input = input("User: ")
    logger.info("Chatbot interaction ended.")
