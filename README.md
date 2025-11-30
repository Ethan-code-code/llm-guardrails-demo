# LLM Guardrails Demo – Rule‑Based Reliability Wrapper

This project is a small prototype that demonstrates how to improve the reliability and safety of a generative AI system using **classical, rule‑based techniques** wrapped around an LLM API. It was built as an application exercise to show practical understanding of guardrails for Generative AI reliability.

## Overview

The application exposes a simple command‑line interface:

- User sends a prompt to this app (not directly to the LLM).
- **Input guardrails** check the prompt for policy violations (harmful content, PII, oversize input).
- If the prompt is allowed, the app calls an LLM (via the OpenAI API).
- **Output guardrails** validate the model's response with the same rules.
- If any check fails, the app returns a **safe fallback message** and logs the reasons instead of the raw LLM output.

All guardrails are implemented using deterministic methods such as keyword lists, regular expressions, and length limits.

## Project structure

```
llm_guardrails_demo/
├── config.py         # Configuration: banned keywords, regex patterns, limits, fallback message
├── guardrails.py     # Pure rule-based checks for prompts and responses
├── llm_client.py     # Thin client for calling the LLM API
├── main.py           # CLI entrypoint wiring guardrails + LLM together
└── requirements.txt  # Python dependencies
```

## Guardrail logic

The prototype focuses on three classical reliability layers:

- **Keyword blocking** – disallows prompts/outputs containing configurable terms such as obvious violence, self‑harm, or financial secrets.
- **PII detection (regex)** – simple regular expressions flag potential email addresses and credit‑card‑like sequences.
- **Length limits** – caps maximum input and output characters to avoid oversized or abusive prompts.

Each guardrail returns a structured result: `{"allowed": bool, "reasons": [str, ...]}`.  
`main.py` uses these results to decide whether to block the request, regenerate, or return the LLM answer.

## Getting started

### Prerequisites

- Python 3.10+ installed
- An OpenAI API key (or compatible LLM key) set in your environment as `OPENAI_API_KEY`

### Installation

1. Clone the repository:

   ```
   git clone https://github.com/<your-username>/llm-guardrails-demo.git
   cd llm_guardrails_demo
   ```

2. (Optional) Create and activate a virtual environment:

   ```
   python -m venv .venv
   # Windows Git Bash / Linux / macOS:
   source .venv/Scripts/activate
   ```

3. Install dependencies:

   ```
   pip install -r requirements.txt
   ```

4. Set your API key for the current shell session:

   ```
   export OPENAI_API_KEY="sk-..."      # Git Bash / macOS / Linux
   # or on Windows PowerShell:
   # $env:OPENAI_API_KEY="sk-..."
   ```

### Running the demo

Call the guarded LLM from the command line with a prompt:

```
python main.py "Explain what machine learning is in simple terms."
```

Example behaviours:

- A normal educational prompt should return:

  ```
  Status: ok
  Answer:
  ...model explanation...
  ```

- A harmful or PII‑containing prompt will be intercepted by the guardrails:

  ```
  Status: blocked_input
  Guardrail reasons:
   - Contains banned keywords: ...
  Answer:
  This request cannot be answered because it violates the safety and reliability policy of this assistant.
  ```

## Design notes

- The **guardrail layer is completely decoupled** from the model client, making it easy to:
  - Swap in a different LLM provider.
  - Extend with additional rules (e.g., domain whitelisting, schema validation).
- The prototype intentionally uses **classical techniques** (keywords, regex, simple thresholds) to emphasize explainability and controllability.
- This setup can be extended with logging, FastAPI/Streamlit front‑ends, or integration into larger RAG / GraphRAG systems.

## Possible extensions

- Add log files capturing prompts, responses, and which rules triggered.
- Introduce schema validation (forcing JSON output) as an additional guardrail.
- Combine rule‑based checks with a small classifier or moderation API for nuanced safety decisions.
- Package as a Docker image or minimal web service.
