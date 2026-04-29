from app.tools.file_parser import parse_file

def file_agent(model, system_prompt, message, file_content=""):
    parsed = parse_file(file_content)

    return model.generate_content(
        f"""{system_prompt}

Analyze this file:
{parsed}

Task:
{message}
"""
    ).text
