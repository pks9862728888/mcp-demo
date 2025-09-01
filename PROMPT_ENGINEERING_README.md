# Prompt Engineering

## Prompt Patterns

### Persona Pattern

Act as persona that is well-versed in xyz. Further instructions.

Prompt size limitations.

For summarization. Summarize below, but retain information on abc

## Root prompt

Strict rules saying what llm can and can not do.

## Question refinement pattern

- From now on, whenever I ask a question, suggest a better version of the question to use instead
- From now on, whenever I ask a question, suggest a better version of the question and ask me if I would like to use it instead

## Cognitive Verifier Pattern

To use the Cognitive Verifier Pattern, your prompt should make the following fundamental contextual statements:

"When you are asked a question, follow these rules

- Generate a number of additional questions that would help more accurately answer the question
- Combine the answers to the individual questions to produce the final answer to the overall question"

## Audience persona pattern

To use this pattern, your prompt should make the following fundamental contextual statements:

Explain X to me.
Assume that I am Persona Y.

Explain how the supply chains for US grocery stores work to me. Assume that I am Ghengis Khan.

## Flipped Interaction pattern

To use this pattern, your prompt should make the following fundamental contextual statements:

I would like you to ask me questions to achieve X
You should ask questions until condition Y is met or to achieve this goal (alternatively, forever)
(Optional) ask me the questions one at a time, two at a time, ask me the first question, etc.

"I would like you to ask me questions to help me diagnose a problem with my Internet. Ask me questions until you have enough information to identify the two most likely causes. Ask me one question at a time. Ask me the first question."

## Few shot examples
