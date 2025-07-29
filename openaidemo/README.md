## To get OPENAI_API_KEY
Create API keys from below: 
https://platform.openai.com/settings/profile/api-keys

## To build agent
Building agents involves assembling components across several domains—such as models, tools, knowledge and memory, audio and speech, guardrails, and orchestration—and OpenAI provides composable primitives for each.

## Use dotenv to load env variables in os environment
```
from dotenv import load_dotenv
load_dotenv()
```

## Theory
The Agents SDK has a very small set of primitives:

Agents, which are LLMs equipped with instructions and tools
Handoffs, which allow agents to delegate to other agents for specific tasks
Guardrails, which enable the inputs to agents to be validated, GuardrailFunctionOutput, InputGuardrailTripwireTriggered
Sessions, which automatically maintains conversation history across agent runs


## Cloning or copying agent is also supported.
By using the clone() method on an agent, you can duplicate an Agent, and optionally change any properties you like.
```
pirate_agent = Agent(
    name="Pirate",
    instructions="Write like a pirate",
    model="o3-mini",
)

robot_agent = pirate_agent.clone(
    name="Robot",
    instructions="Write like a robot",
)
```

## Forcing tool use
Supplying a list of tools doesn't always mean the LLM will use a tool. You can force tool use by setting ModelSettings.tool_choice

```
agent = Agent(
    name="Weather Agent",
    instructions="Retrieve weather details.",
    tools=[get_weather],
    model_settings=ModelSettings(tool_choice="get_weather") 
)
```

## To create a tool
Annotate method by @function_tool

## If multiple tools are called then we can stop on any tool
"""
agent = Agent(
    name="Stop At Stock Agent",
    instructions="Get weather or sum numbers.",
    tools=[get_weather, sum_numbers],
    tool_use_behavior=StopAtTools(stop_at_tool_names=["get_weather"])
)
"""
