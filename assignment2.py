from common import logger
from common.logger import Logger
from common.llm_api import generate_response
from common.extract_response import extract_code_from_response
from common.prompts import PromptSet


def get_initial_prompts(language, func_descr) -> PromptSet:
    ps = PromptSet()
    ps.add_system_prompt(
        f"""You are an expert {language} programmer being asked to write a function.
            Respond only with the function and no comments or explanations."
    """)

    ps.add_user_prompt(f"Write a {language} function to {func_descr}.")
    return ps


def get_second_prompt_set(language, first_prompt_set: PromptSet, code):
    second_prompt = """
    Add comprehensive documentation to the code and make sure to include:
        Function description
        Parameter descriptions
        Return value description
        Example usage
        Edge cases
    Respond only with the function and its comments"""

    first_prompt_set.add_agent_code_response(language, code)
    first_prompt_set.add_user_prompt(second_prompt)
    return first_prompt_set


def get_third_prompt_set(language, second_prompt_set: PromptSet, new_code):
    third_prompt = """
        Add test cases using Python’s unittest framework
        The new tests should cover:
            Basic functionality
            Edge cases
            Error cases
            Various input scenarios"""
    second_prompt_set.add_agent_code_response(language, new_code)
    second_prompt_set.add_user_prompt(third_prompt)
    return second_prompt_set


def get_function_description():
    return input("What would you like the function to do?")


def agent_loop(lg: Logger, task):
    language = "python"
    ps = get_initial_prompts(language, task)
    response = generate_response(ps)
    lg.DEBUG_BLOCK("First Response:", response)
    code = extract_code_from_response(lg, language, response)
    lg.DEBUG_BLOCK("CODE: ", code)

    ps = get_second_prompt_set(language, ps, code)
    response = generate_response(ps)
    new_code = extract_code_from_response(lg, language, response)
    lg.DEBUG_BLOCK("CODE: ", new_code)

    ps = get_third_prompt_set(language, ps, code)
    response = generate_response(ps)
    new_code = extract_code_from_response(lg, language, response)

    lg.set_verbose()
    lg.DEBUG_BLOCK("CODE: ", new_code)
    lg.set_quite()


def main():
    lg = Logger(logger.MODE_QUITE)
    # function_description = get_function_description()
    function_description = "sort a bunch of numbers"
    lg.OUTPUT(f"Creating function to perform >{function_description}<")
    agent_loop(lg, function_description)


if __name__ == "__main__":
    main()
