import json

from common import logger
from common.logger import Logger
from common.llm_api import generate_response_with_tools
from common.prompts import PromptSet

from Assignment4Tools.tools import tools, tool_registry, SYSTEM_PROMPT


def agent_loop(lg: Logger, task):
    """
        GAIL:
            Goals
            Actions
            Instructions
            Language    (Description of language used to perform actions)
        GAME:
            Goals
            Actions that can be taken to achieve goals
            Memory
            Execution environment
    """
    iteration = 0
    max_iterations = 10

    # Initial setup
    agent_rules = PromptSet()
    agent_rules.add_system_prompt(SYSTEM_PROMPT)
    memory = PromptSet()
    memory.add_user_prompt(task)

    # The Agent Loop
    # 1. Construct prompt: Combine agent rules with memory
    # 2. Generate response from LLM
    # 3. Parse response to determine action
    # 4. Execute Action
    # 5. Update memory with response and results
    # 6. Check termination condition
    while iteration < max_iterations:
        # 1. Construct prompt: Combine agent rules with memory
        prompt = agent_rules + memory

        # 2. Generate response from LLM
        lg.DEBUG("Agent thinking...")
        tool_resp, tool_resp_ok = generate_response_with_tools(prompt, tools)
        lg.DEBUG(f"Agent response: {tool_resp}")

        # 3. Parse response to determine action
        if tool_resp_ok:
            tool_name = tool_resp.function.name
            tool_args = json.loads(tool_resp.function.arguments)
        else:
            try:
                j_resp = json.loads(tool_resp)
                tool_name = j_resp["name"]
                tool_args = j_resp["args"]
            except:
                lg.OUTPUT(f"EARLY TERMINATION: {tool_resp}")
                break

        lg.set_verbose()
        lg.DEBUG(f"Action: {tool_name}({tool_args})")
        lg.set_quite()

        # 4. Execute Action
        if tool_name in tool_registry:
            try:
                result = tool_registry[tool_name](**tool_args)
            except Exception as e:
                result = {"error": f"Error executing {tool_name}: {str(e)}"}
        else:
            result = {"error": f"Unknown tool: {tool_name}"}

        lg.DEBUG(f"Result: {result}")

        # 5. Update memory with response and results
        action = {
            "tool_name": tool_name,
            "args": tool_args
        }
        memory.add_agent_response(json.dumps(action))
        memory.add_user_prompt(json.dumps(result))

        # 6. Check termination condition
        if tool_name == "terminate":
            break

        iteration += 1


def main():
    lg = Logger(logger.MODE_QUITE)
    agent_loop(lg, "What is the longest word in the third file")


if __name__ == "__main__":
    main()
