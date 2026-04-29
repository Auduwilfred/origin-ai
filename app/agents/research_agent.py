from app.tools.web_search import web_search

def research_agent(model, system_prompt, message):
    search_result = web_search(message)

    return model.generate_content(
        f"""{system_prompt}

Use this data:
{search_result}

Answer clearly:
{message}
"""
    ).text
