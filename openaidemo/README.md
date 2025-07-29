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
Guardrails, which enable the inputs to agents to be validated
Sessions, which automatically maintains conversation history across agent runs
