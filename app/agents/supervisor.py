def route_task(message: str):
    msg = message.lower()

    if any(x in msg for x in ["build", "create", "develop", "code"]):
        return "build"

    elif any(x in msg for x in ["research", "latest", "news", "find"]):
        return "research"

    elif any(x in msg for x in ["file", "analyze", "document"]):
        return "file"

    else:
        return "chat"
