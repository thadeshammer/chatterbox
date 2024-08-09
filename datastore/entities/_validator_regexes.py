# datastore/entities/_validator_regexes.py
# A centralized spot for regexes used in data validation in API requests and responses.
import re
from typing import Any

APP_UUID4_REGEX = (
    r"^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$"
)
LANGUAGE_CODE_REGEX = r"^[a-z]{2}$"
LOGIN_NAME_REGEX = r"^[a-z0-9_]{1,25}$"
NICKNAME_REGEX = r"^[a-zA-Z0-9_ ]{1,25}$"


def matches_regex(value: Any, pattern: str) -> str:
    """Check if the given value matches the provided regex pattern."""
    if not isinstance(value, str) or not bool(re.match(pattern, value)):
        raise ValueError
    return value
