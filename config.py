# config.py

# Keywords you want to block in prompts and responses
BANNED_KEYWORDS = [
    "kill",
    "suicide",
    "bomb",
    "terrorist",
    "credit card",
    "social security number",
]

# Regex patterns to detect simple PII patterns
PII_PATTERNS = {
    "credit_card": r"\b(?:\d[ -]*?){13,16}\b",
    "email": r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
}

# Length limits to avoid huge prompts/outputs
MAX_INPUT_CHARS = 800
MAX_OUTPUT_CHARS = 800

# Standard message returned when something is blocked
SAFE_FALLBACK_MESSAGE = (
    "This request cannot be answered because it violates the safety "
    "and reliability policy of this assistant."
)
