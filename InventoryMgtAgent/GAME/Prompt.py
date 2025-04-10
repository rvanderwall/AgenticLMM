from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class Prompt:
    messages: List[Dict] = field(default_factory=list)
    tools: List[Dict] = field(default_factory=list)
    metadata: dict = field(default_factory=dict)  # Fixing mutable default issue


class PromptSet:
    def __init__(self):
        self.prompts = []

    def __add__(self, other):
        prompts = []
        for prompt in self.prompts:
            prompts.append(prompt)
        for prompt in other.prompts:
            prompts.append(prompt)
        ps = PromptSet()
        ps.prompts = prompts
        return ps

    def add_system_prompt(self, sys_prompt):
        new_prompt = {"role": "system",
                      "content": sys_prompt}
        self.prompts.append(new_prompt)

    def add_user_prompt(self, user_prompt):
        new_prompt = {"role": "user",
                      "content": user_prompt}
        self.prompts.append(new_prompt)

    def add_agent_response(self, agent_response):
        new_prompt = {"role": "assistant",
                      "content": agent_response}
        self.prompts.append(new_prompt)

    def add_agent_code_response(self, language, code_block):
        agent_response = f"```{language}\n\n" + code_block + "\n\n```"
        new_prompt = {"role": "assistant",
                      "content": agent_response}
        self.prompts.append(new_prompt)

    def get_prompts(self) -> List[Dict]:
        return self.prompts
