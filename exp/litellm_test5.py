# Important!!!
#
# <---- Set your 'OPENAI_API_KEY' as a secret over there with the "key" icon
#
#
import os
from litellm import completion
from typing import List, Dict


def generate_response(messages: List[Dict]) -> str:
    """Call LLM to get response"""
    response = completion(
        model="openai/gpt-4o",
        messages=messages,
        max_tokens=1024
    )
    return response.choices[0].message.content

messages = [
   {"role": "system", "content": "You are an expert software engineer that prefers functional programming."},
   {"role": "user", "content": "Write a function to swap the keys and values in a dictionary."}
]

response = generate_response(messages)
print(response)

# Here is the assistant's response from the previous step
# with the code. This gives it "memory" of the previous
# interaction.
messages.append({"role": "assistant", "content": response})

# Now, we can ask the assistant to update the function
messages.append({"role": "user", "content": "Update the function to include documentation."})


response = generate_response(messages)
print(response)

