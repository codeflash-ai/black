"""
Formatting numeric literals.
"""

from blib2to3.pytree import Leaf


def format_hex(text: str) -> str:
    """
    Formats a hexadecimal string like "0x12B3"
    """
    before, after = text[:2], text[2:]
    return f"{before}{after.upper()}"


def format_scientific_notation(text: str) -> str:
    """Formats a numeric string utilizing scientific notation. Avoids unnecessary operations."""
    before, after = text.split("e")
    if after.startswith("-"):
        return f"{format_float_or_int_string(before)}e-{after[1:]}"
    elif after.startswith("+"):
        return f"{format_float_or_int_string(before)}e{after[1:]}"
    return f"{format_float_or_int_string(before)}e{after}"


def format_complex_number(text: str) -> str:
    """Formats a complex string like `10j`"""
    number = text[:-1]
    suffix = text[-1]
    return f"{format_float_or_int_string(number)}{suffix}"


def format_float_or_int_string(text: str) -> str:
    """Formats a float string like "1.0". Only splits if needed."""
    if "." in text:
        before, after = text.split(".")
        return f"{before or 0}.{after or 0}"
    return text


def normalize_numeric_literal(leaf: Leaf) -> None:
    """Normalizes numeric (float, int, and complex) literals.

    All letters used in the representation are normalized to lowercase."""
    text = leaf.value.lower()
    if text.startswith(("0o", "0b")):
        # Leave octal and binary literals alone.
        pass
    elif text.startswith("0x"):
        text = format_hex(text)
    elif "e" in text:
        text = format_scientific_notation(text)
    elif text.endswith("j"):
        text = format_complex_number(text)
    else:
        text = format_float_or_int_string(text)
    leaf.value = text
