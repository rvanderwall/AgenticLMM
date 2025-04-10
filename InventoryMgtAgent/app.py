
from GAME.Goals import Goal
from GAME.Environment import Environment
from GAME.Agent import Agent

from function_calling_action_language import AgentFunctionCallingActionLanguage
from python_action_registry import PythonActionRegistry
from openAI_api import generate_response


def main():
    # Define the agent's goals
    goals = [
        Goal(priority=1,
             name="Gather Information",
             description="Read each file in the project in order to build a deep understanding of the project in order to write a README"),
        Goal(priority=1,
             name="Terminate",
             description="Call terminate when done and provide a complete README for the project in the message parameter")
    ]

    # Define the agent language and environment
    agent_language = AgentFunctionCallingActionLanguage()

    from Assignment5.GAME.tool_registration import G_tools
    print(f"{len(G_tools)} tools registered.")
    from actions import G_tools
    print(f"{len(G_tools)} tools registered.")
    action_registry = PythonActionRegistry(G_tools, tags=["file_operations", "system"])
    environment = Environment()

    # Create the agent
    agent = Agent(
        goals=goals,
        agent_language=agent_language,
        action_registry=action_registry,
        generate_response=generate_response,
        environment=environment
    )

    # Run the agent
    user_input = "Write a README for this project."
    final_memory = agent.run(user_input, max_iterations=10)
    print(final_memory.get_memories())

    # Print the termination message (if any)
    for item in final_memory.get_memories():
        print(f"\nMemory: {item['content']}")


if __name__ == "__main__":
    main()
