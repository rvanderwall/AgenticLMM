from common.logger import Logger


def extract_code_from_response(lg: Logger, language, response_text):
    if '```' not in response_text:
        return response_text

    parts = response_text.split("```")
    if len(parts) != 3:
        lg.ERROR(f"CANNOT FIND CODE BLOCK IN RESPONSE: {response_text}")
        return None

    code_block = parts[1]
    if language not in code_block:
        lg.ERROR(f"CANNOT FIND {language} CODE IN RESPONSE: {code_block}")

    code_block = code_block[len(language):]
    return code_block


def extract_json_from_response(lg: Logger, json_block_tag, response_text):
    if '```' not in response_text:
        return response_text

    parts = response_text.split("```")
    if len(parts) != 3:
        response_text = f"CANNOT FIND JSON BLOCK IN RESPONSE: {response_text}"
        lg.ERROR(response_text)
        return response_text

    json_block = parts[1]
    if json_block_tag not in json_block:
        response_text = f"CANNOT FIND {json_block_tag} IN RESPONSE: {json_block}"
        lg.ERROR(response_text)
        return response_text

    json_block = json_block[len(json_block_tag):]
    return json_block
