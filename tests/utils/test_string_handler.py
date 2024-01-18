from utils.string_handler import escape_markdown, truncate_text


def test_escape_markdown():
    assert escape_markdown("*bold*") == "\\*bold\\*"
    assert escape_markdown("_italic_") == "\\_italic\\_"
    assert escape_markdown("[link](url)") == "\\[link\\]\\(url\\)"


def test_truncate_text():
    assert truncate_text("Hello World", 5) == "..."
    assert truncate_text("Hello World", 20) == "Hello World"
    assert truncate_text("Hello World", 8, "~~~") == "Hello~~~"
    assert truncate_text("Hello World", 3, "") == "Hel"
