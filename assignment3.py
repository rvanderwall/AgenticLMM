import json
import os
from typing import Dict

from common import logger
from common.logger import Logger
from common.llm_api import generate_response
from common.prompts import PromptSet


def get_agent_rules() -> PromptSet:
    ps = PromptSet()
    # The system prompt should include:
    #    Goals (Persona, rules, processes)
    #    Actions (Understanding of tools it has access to)
    #    Language (Specific syntax, constraints)
    ps.add_system_prompt(
        """
            You are an AI agent that can perform tasks by using available tools.
            Available tools:
            - list_files() -> List[str]: List all files in the current directory.
            - read_file(file_name: str) -> str: Read the content of a file.
            - terminate(message: str): End the agent loop and print a summary to the user.

            If a user asks about files, list them before reading.

            Every response MUST have an action.
            Respond in this format:

            ```action
            {
                "tool_name": "insert tool_name",
                "args": {...fill in any required arguments here...}
            }```
        """)
    return ps


def list_python_files():
    """Returns a list of all Python files in the src/ directory."""
    return [f for f in os.listdir(".") if f.endswith(".py")]


def parse_action(response: str) -> Dict:
    """Parse the LLM response into a structured action dictionary."""
    try:
        response = extract_markdown_block(response, "action")
        response_json = json.loads(response)
        if "tool_name" in response_json and "args" in response_json:
            return response_json
        else:
            return {"tool_name": "error", "args": {"message": "You must respond with a JSON tool invocation."}}
    except json.JSONDecodeError:
        return {"tool_name": "error", "args": {"message": "Invalid JSON response. You must respond with a JSON tool invocation."}}


def execute_action(lg: Logger, action: Dict):
    if action["tool_name"] == "list_files":
        result = {"result": list_python_files()}
    elif action["tool_name"] == "read_file":
        result = {"result": read_file(action["args"]["file_name"])}
    elif action["tool_name"] == "error":
        result = {"error": action["args"]["message"]}
    elif action["tool_name"] == "terminate":
        lg.OUTPUT(action["args"]["message"])
        return None
    else:
        result = {"error": "Unknown action: " + action["tool_name"]}

    return result


def agent_loop(lg: Logger):
    iterations = 0
    max_iterations = 10
    agent_rules = get_agent_rules()
    memory = PromptSet()

    # The Agent Loop
    while iterations < max_iterations:
        # 1. Construct prompt: Combine agent rules with memory
        prompt = agent_rules + memory

        # 2. Generate response from LLM
        lg.DEBUG("Agent thinking...")
        response = generate_response(prompt)
        lg.DEBUG(f"Agent response: {response}")

        # 3. Parse response to determine action
        action = parse_action(response)

        # 4. Execute Action
        result = execute_action(lg, action)
        if result is None:
            break

        lg.DEBUG(f"Action result: {result}")

        # 5. Update memory with response and results
        memory.add_agent_response(response)
        memory.add_user_prompt(json.dumps(result))

        # 6. Check termination condition
        if action["tool_name"] == "terminate":
            break

        iterations += 1


def main():
    lg = Logger(logger.MODE_QUITE)
    agent_loop(lg)


if __name__ == "__main__":
    main()
