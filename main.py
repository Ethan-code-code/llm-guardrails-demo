# main.py
import argparse
from guardrails import run_input_guardrails, run_output_guardrails
from config import SAFE_FALLBACK_MESSAGE
from llm_client import call_llm


def chat_once(prompt: str) -> dict:
    # 1) Input guardrails
    input_result = run_input_guardrails(prompt)
    if not input_result["allowed"]:
        return {
            "status": "blocked_input",
            "reasons": input_result["reasons"],
            "answer": SAFE_FALLBACK_MESSAGE,
        }

    # 2) Call the LLM
    raw_answer = call_llm(prompt)

    # 3) Output guardrails
    output_result = run_output_guardrails(raw_answer)
    if not output_result["allowed"]:
        return {
            "status": "blocked_output",
            "reasons": output_result["reasons"],
            "answer": SAFE_FALLBACK_MESSAGE,
        }

    return {
        "status": "ok",
        "reasons": [],
        "answer": raw_answer,
    }


def main():
    parser = argparse.ArgumentParser(
        description="LLM Guardrail Demo: rule-based reliability wrapper."
    )
    parser.add_argument(
        "prompt",
        type=str,
        help="User prompt to send to the guarded LLM.",
    )
    args = parser.parse_args()

    result = chat_once(args.prompt)
    print("Status:", result["status"])
    if result["reasons"]:
        print("Guardrail reasons:")
        for r in result["reasons"]:
            print(" -", r)
    print("\nAnswer:\n", result["answer"])


if __name__ == "__main__":
    main()
