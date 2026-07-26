import re


# --------------------------------------------------
# Remove URLs
# --------------------------------------------------

def remove_urls(text: str) -> str:
    """
    Remove URLs from text.
    """
    return re.sub(r"http\S+|www\S+", "", text)


# --------------------------------------------------
# Remove HTML tags
# --------------------------------------------------

def remove_html(text: str) -> str:
    """
    Remove HTML tags if any remain.
    """
    return re.sub(r"<.*?>", "", text)


# --------------------------------------------------
# Normalize whitespace
# --------------------------------------------------

def normalize_whitespace(text: str) -> str:
    """
    Replace tabs, newlines and multiple spaces
    with a single space.
    """

    text = text.replace("\n", " ")
    text = text.replace("\r", " ")
    text = text.replace("\t", " ")

    text = re.sub(r"\s+", " ", text)

    return text.strip()


# --------------------------------------------------
# Remove unwanted invisible Unicode characters
# --------------------------------------------------

def remove_invisible_chars(text: str) -> str:
    """
    Remove zero-width spaces and similar invisible characters.
    """

    invisible = [
        "\u200b",
        "\u200c",
        "\u200d",
        "\ufeff"
    ]

    for char in invisible:
        text = text.replace(char, "")

    return text


# --------------------------------------------------
# Main preprocessing function
# --------------------------------------------------

def preprocess_text(text) -> str:
    """
    Complete preprocessing pipeline.
    """

    if text is None:
        return ""

    text = str(text)

    text = remove_html(text)

    text = remove_urls(text)

    text = remove_invisible_chars(text)

    text = normalize_whitespace(text)

    return text