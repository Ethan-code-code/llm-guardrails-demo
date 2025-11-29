# guardrails.py
import re
from typing import List, Dict, Any
from config import (
    BANNED_KEYWORDS,
    PII_PATTERNS,
    MAX_INPUT_CHARS,
    MAX_OUTPUT_CHARS,
)


def _check_length(text: str, max_chars: int, kind: str) -> Dict[str, Any]:
    if len(text) > max_chars:
        return {
            "allowed": False,
            "reasons": [f"{kind} too long: {len(text)} > {max_chars} characters"],
        }
    return {"allowed": True, "reasons": []}


def _check_banned_keywords(text: str) -> Dict[str, Any]:
    lowered = text.lower()
    triggered = [kw for kw in BANNED_KEYWORDS if kw in lowered]
    if triggered:
        return {
            "allowed": False,
            "reasons": [f"Contains banned keywords: {', '.join(triggered)}"],
        }
    return {"allowed": True, "reasons": []}


def _check_pii_patterns(text: str) -> Dict[str, Any]:
    hits: List[str] = []
    for name, pattern in PII_PATTERNS.items():
        if re.search(pattern, text):
            hits.append(name)
    if hits:
        return {
            "allowed": False,
            "reasons": [f"Detected potential PII patterns: {', '.join(hits)}"],
        }
    return {"allowed": True, "reasons": []}


def run_input_guardrails(prompt: str) -> Dict[str, Any]:
    """
    Run all rule-based checks on the user prompt.
    Returns dict: {"allowed": bool, "reasons": [str, ...]}.
    """
    checks = [
        _check_length(prompt, MAX_INPUT_CHARS, "Input"),
        _check_banned_keywords(prompt),
        _check_pii_patterns(prompt),
    ]

    reasons: List[str] = []
    for result in checks:
        if not result["allowed"]:
            reasons.extend(result["reasons"])

    return {"allowed": len(reasons) == 0, "reasons": reasons}


def run_output_guardrails(response: str) -> Dict[str, Any]:
    """
    Run all rule-based checks on the model response.
    Returns dict: {"allowed": bool, "reasons": [str, ...]}.
    """
    checks = [
        _check_length(response, MAX_OUTPUT_CHARS, "Output"),
        _check_banned_keywords(response),
        _check_pii_patterns(response),
    ]

    reasons: List[str] = []
    for result in checks:
        if not result["allowed"]:
            reasons.extend(result["reasons"])

    return {"allowed": len(reasons) == 0, "reasons": reasons}
