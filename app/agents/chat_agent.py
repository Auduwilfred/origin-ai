def chat_agent(model, system_prompt, message):
    return model.generate_content(
        f"{system_prompt}\n\nUser:\n{message}"
    ).text
