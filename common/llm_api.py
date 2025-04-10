from typing import List

from litellm import completion
from common.prompts import PromptSet


def generate_response(prompt_set: PromptSet) -> str:
    """Call LLM to get response"""
    response = completion(
        model="openai/gpt-4o",
        messages=prompt_set.get_prompts(),
        max_tokens=1024
    )
    return response.choices[0].message.content


def generate_response_with_tools(prompt_set: PromptSet, tools: List):
    """Call LLM to get response"""
    response = completion(
        model="openai/gpt-4o",
        messages=prompt_set.get_prompts(),
        tools=tools,
        max_tokens=1024,
    )

    message = response.choices[0].message
    if message.tool_calls:
        return message.tool_calls[0], True
    else:
        return message.content, False
