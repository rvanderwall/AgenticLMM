from typing import List

from Assignment5.GAME.Actions import Action
from Assignment5.GAME.Goals import Goal
from Assignment5.GAME.Environment import Environment
from Assignment5.GAME.Memory import Memory
from Assignment5.GAME.Prompt import Prompt


class AgentLanguage:
    def __init__(self):
        pass

    def construct_prompt(self,
                         actions: List[Action],
                         environment: Environment,
                         goals: List[Goal],
                         memory: Memory) -> Prompt:
        raise NotImplementedError("Subclasses must implement this method")

    def parse_response(self, response: str) -> dict:
        raise NotImplementedError("Subclasses must implement this method")

