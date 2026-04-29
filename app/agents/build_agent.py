def build_agent(model, system_prompt, message):
    return model.generate_content(
        f"""{system_prompt}

You are a senior software engineer.

Generate:
- architecture
- full code
- explanations

Request:
{message}
"""
    ).text
