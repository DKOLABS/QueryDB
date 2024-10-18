import re
import unicodedata


def make_safe_filename(search_name):
    # Normalize the string to NFKD form, which separates characters and their diacritics
    normalized_name = unicodedata.normalize("NFKD", search_name)

    # Encode to ASCII bytes, ignoring characters that can't be represented in ASCII
    ascii_encoded_name = normalized_name.encode("ASCII", "ignore")

    # Decode back to a string
    ascii_name = ascii_encoded_name.decode("ASCII")

    # Replace spaces with underscores
    safe_name = re.sub(r"\s+", "_", ascii_name)

    # Remove any remaining unsafe characters
    safe_name = re.sub(r"[^A-Za-z0-9_\-\.]", "", safe_name)

    # Ensure the filename is not empty
    if not safe_name:
        safe_name = "default_filename"

    return safe_name
