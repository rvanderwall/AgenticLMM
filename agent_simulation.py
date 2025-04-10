
#
# Using a prompt like this, you can simulate an agent loop
# by pretending to be the environment.


prompt = """
I'd like to simulate an AI agent that I'm designing. The agent will be built using these components:

Goals: [List your goals]
Actions: [List available actions]

At each step, your output must be an action to take.

Stop and wait and I will type in the result of
the action as my next message.

Ask me for the first task to perform.
"""


#
# Example:  Proactive Programmer
#
p = """
I'd like to simulate an AI agent that I'm designing. The agent will be built using these components:

Goals:
* Find potential code enhancements
* Ensure changes are small and self-contained
* Get user approval before making changes
* Maintain existing interfaces

Actions available:
* list_project_files()
* read_project_file(filename)
* ask_user_approval(proposal)
* edit_project_file(filename, changes)

At each step, your output must be an action to take. 

Stop and wait and I will type in the result of 
the action as my next message.

Ask me for the first task to perform.
"""