from app.tools.google_search import google_search

def research_agent(model, system_prompt, message):

    search_results = google_search(message)

    context = "\n".join([
        f"{r.get('title')} - {r.get('snippet')} ({r.get('link')})"
        for r in search_results if "error" not in r
    ])

    prompt = f"""
{system_prompt}

You are a real-time grounded AI.

Use ONLY this live web data:

{context}

USER QUESTION:
{message}

Rules:
- Be accurate
- If data conflicts, mention it
- Prefer latest information
"""

    return model.generate_content(prompt).text
