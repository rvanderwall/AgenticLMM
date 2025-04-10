from typing import List
import os

from common.logger import Logger, MODE_QUITE


def list_python_files() -> List[str]:
    """Returns a list of all Python files in the src/ directory."""
    return [f for f in os.listdir(".") if f.endswith(".py")]


LIST_FILES_TOOL_DESCRIPTION = {
        "type": "function",
        "function": {
            "name": "list_python_files",
            "description": "Returns a list of files in the directory.",
            "parameters": {"type": "object", "properties": {}, "required": []}
        }
    }


def read_python_file(file_name):
    """Reads a Python file from the src/ directory with error handling."""
    file_path = os.path.join(".", file_name)

    if not file_name.endswith(".py"):
        return {"error": """Invalid file type. Only Python files can be read. 
                            Call the list_python_files function to get a list of valid files."""}

    if not os.path.exists(file_path):
        return {"error": f"""File '{file_name}' does not exist in the src/ directory.
                            Call the list_python_files function to get a list of valid files."""}

    with open(file_path, "r") as f:
        return {"content": f.read()}


READ_FILE_TOOL_DESCRIPTION = {
    "type": "function",
    "function": {
        "name": "read_python_file",
        "description": "Reads the content of a Python file from the src/ directory.",
        "parameters": {
            "type": "object",
            "properties": {"file_name": {"type": "string"}},
            "required": ["file_name"]
        }
    }
}


def write_documentation_file(file_name: str, content: str):
    return


WRITE_DOCUMENT_TOOL_DESCRIPTION = {
    "type": "function",
    "function": {
        "name": "write_documentation_file",
        "description": "Writes a documentation file to the docs/ directory.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_name": {"type": "string"},
                "content": {"type": "string"}
            },
            "required": ["file_name", "content"]
        }
    }
}


def terminate(message: str) -> None:
    """Terminate the agent loop and provide a summary message."""
    lg = Logger(MODE_QUITE)
    lg.OUTPUT(f"Termination message: {message}")


TERMINATE_TOOL_DESCRIPTION = {
    "type": "function",
    "function": {
        "name": "terminate",
        "description": "Terminates the conversation. No further actions or interactions are possible after this. Prints the provided message for the user.",
        "parameters": {
            "type": "object",
            "properties": {
                "message": {"type": "string"}
            },
            "required": ["message"]
        }
    }
}


tool_registry = {
    "list_python_files": list_python_files,
    "read_python_file": read_python_file,
    "write_documentation_file": write_documentation_file,
    "terminate": terminate
}


tools = [LIST_FILES_TOOL_DESCRIPTION,
         READ_FILE_TOOL_DESCRIPTION,
         WRITE_DOCUMENT_TOOL_DESCRIPTION,
         TERMINATE_TOOL_DESCRIPTION
         ]


# The system prompt should include:
#    Goals (Persona, rules, processes)
#    Actions (Understanding of tools it has access to)
#    Language (Specific syntax, constraints)
SYSTEM_PROMPT = """
    You are an AI agent that can perform tasks by using available tools.
    If a user asks about files, documents, or content, first list the files before reading them.

    When you are done, terminate the conversation by using the "terminate" tool and 
    I will provide the results to the user.
"""
