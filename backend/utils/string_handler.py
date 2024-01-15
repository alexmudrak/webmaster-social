async def escape_markdown(text: str) -> str:
    escape_chars = "_*[]()~`>#+-=|{}.!"
    return "".join(
        f"\\{char}" if char in escape_chars else char for char in text
    )
