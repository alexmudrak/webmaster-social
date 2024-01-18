import textwrap


def escape_markdown(text: str) -> str:
    """
    Markdown special characters like *, _, and [] will be escaped with a
    backslash so that they are treated as literal characters when the text
    is rendered in markdown.
    """
    escape_chars = "_*[]()~`>#+-=|{}.!"
    return "".join(
        f"\\{char}" if char in escape_chars else char for char in text
    )


def truncate_text(text: str, max_length: int, placeholder: str = "...") -> str:
    """
    Truncate a message to a maximum length, ensuring that the truncation
    occurs at a word boundary and ends with an ellipsis if truncated.
    """
    check_length = max_length - len(placeholder)

    if check_length < 0:
        return textwrap.shorten(
            text,
            width=max_length,
            placeholder="",
        )

    return textwrap.shorten(
        text,
        width=max_length,
        placeholder=placeholder,
    )
