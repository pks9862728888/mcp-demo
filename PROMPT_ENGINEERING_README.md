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

Chain of thought prompting

Examples should align with the input pattern which we are trying to predict.
So enough relevant examples are required.
Example:
Reasoning:
Answer:

## ReAct prompting

Task: to do
Think: what I need to do
Action: search internet
Result: respond outcome

## Using llm to grade each other

One model produces output
Another model / models evaluates it and grades output

## Game play pattern

To use this pattern, your prompt should make the following fundamental contextual statements:

Create a game for me around X OR we are going to play an X game
One or more fundamental rules of the game

### Template pattern

To use this pattern, your prompt should make the following fundamental contextual statements:

I am going to provide a template for your output

X is my placeholder for content
Try to fit the output into one or more of the placeholders that I list
Please preserve the formatting and overall template that I provide
This is the template: PATTERN with PLACEHOLDERS
You will need to replace "X" with an appropriate placeholder, such as "CAPITALIZED WORDS" or "<PLACEHOLDER>". You will then need to specify a pattern to fill in, such as "Dear <FULL NAME>" or "NAME, TITLE, COMPANY".

### Meta language creation pattern

When I say "variations(<something>)", I mean give me ten different variations of <something>

Usage: "variations(company names for a company that sells software services for prompt engineering)"
Usage: "variations(a marketing slogan for pickles)"

### Recipe pattern

I would like to purchase a house. I know that I need to perform steps make an offer and close on the house. Provide a complete sequence of steps for me. Fill in any missing steps.

### Alternative approaches pattern

To use this pattern, your prompt should make the following fundamental contextual statements:

If there are alternative ways to accomplish a task X that I give you, list the best alternate approaches

(Optional) compare/contrast the pros and cons of each approach
(Optional) include the original way that I asked
(Optional) prompt me for which approach I would like to use

## Ask for input pattern

From now on, I am going to cut/paste email chains into our conversation. You will summarize what each person's points are in the email chain. You will provide your summary as a series of sequential bullet points. At the end, list any open questions or action items directly addressed to me. My name is Jill Smith.
Ask me for the first email chain.

## Outline expansion pattern

Act as an outline expander. Generate a bullet point outline based on the input that I give you and then ask me for which bullet point you should expand on. Each bullet can have at most 3-5 sub bullets. The bullets should be numbered using the pattern [A-Z].[i-v].[* through ****]. Create a new outline for the bullet point that I select. At the end, ask me for what bullet point to expand next. Ask me for what to outline.

## Actions pattern

Whenever I type: "add FOOD", you will add FOOD to my grocery list and update my estimated grocery bill. Whenever I type "remove FOOD", you will remove FOOD from my grocery list and update my estimated grocery bill. Whenever I type "save" you will list alternatives to my added FOOD to save money. At the end, you will ask me for the next action.  
Ask me for the first action.

## Fact check list pattern

Whenever you output text, generate a set of facts that are contained in the output. The set of facts should be inserted at the end of the output. The set of facts should be the fundamental facts that could undermine the veracity of the output if any of them are incorrect.

## Tail generation pattern

Act as an outline expander. Generate a bullet point outline based on the input that I give you and then ask me for which bullet point you should expand on. Create a new outline for the bullet point that I select. At the end, ask me for what bullet point to expand next.  
Ask me for what to outline.

## Semantic filter pattern

Filter this information to remove any personally identifying information or information that could potentially be used to re-identify the person.

## Policy highlighter

Dont list any names or dates. Read and understand the travel policy. Then think step by step. Does this receipt comply with the travel policy?
