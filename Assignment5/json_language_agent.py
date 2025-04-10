from typing import List
import json

from Assignment5.GAME.Actions import Action
from Assignment5.GAME.AgentLanguage import AgentLanguage


class AgentJsonActionLanguage(AgentLanguage):
    action_format = """
<Stop and think step by step. Insert your thoughts here.>

```action
{
    "tool": "tool_name",
    "args": {...fill in arguments...}
}
```"""

    def format_actions(self, actions: List[Action]) -> List:
        # Convert actions to a description the LLM can understand
        action_descriptions = [
            {
                "name": action.name,
                "description": action.description,
                "args": action.parameters
            }
            for action in actions
        ]

        return [{
            "role": "system",
            "content": f"""
Available Tools: {json.dumps(action_descriptions, indent=4)}

{self.action_format}
"""
        }]

    def parse_response(self, response: str) -> dict:
        """Extract and parse the action block"""
        try:
            start_marker = "```action"
            end_marker = "```"

            stripped_response = response.strip()
            start_index = stripped_response.find(start_marker)
            end_index = stripped_response.rfind(end_marker)
            json_str = stripped_response[
                       start_index + len(start_marker):end_index
                       ].strip()

            return json.loads(json_str)
        except Exception as e:
            print(f"Failed to parse response: {str(e)}")
            raise e
