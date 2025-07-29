from agents import Agent, Runner
from dotenv import load_dotenv

load_dotenv()

agent = Agent(
    name="Coder",
    instructions="You are a code assistant. You are given a task and you need to write the code to complete the task.",
    model="gpt-4.1",
)


def simple_hello_world_agent():
    result = Runner.run_sync(agent, input="Write a java program to print hello world.")
    print(result.final_output)


def main():
    simple_hello_world_agent()


if __name__ == "__main__":
    main()
