import os
import re
from pathlib import Path
from dotenv import load_dotenv

env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), ".env")
load_dotenv(env_path, encoding="utf-8")

try:
    from groq import Groq
    _GROQ_AVAILABLE = True
except ImportError:
    _GROQ_AVAILABLE = False

_client = None


def _get_client():
    global _client
    if _client is None and _GROQ_AVAILABLE:
        api_key = os.getenv("GROQ_API_KEY")
        if api_key:
            _client = Groq(api_key=api_key)
    return _client


# Module-level client instance (falls back gracefully if not configured)
client = _get_client()


def generate_explanation(risk_analysis: dict) -> dict:
    """
    Uses Groq (free) to generate plain-English clause explanations.
    Model: qwen/qwen3.6-27b or llama-3.1-8b-instant
    """
    clause_text = risk_analysis.get("clause_text", "")
    clause_type = risk_analysis.get("type", "Unknown")
    risk_level  = risk_analysis.get("risk_level", "LOW")
    risk_reason = risk_analysis.get("risk_reason", "")

    prompt = f"""You are a legal analyst reviewing an NDA (Non-Disclosure Agreement).

Clause type: {clause_type}
Risk level: {risk_level}
Risk reason: {risk_reason}

Clause text:
\"\"\"{clause_text[:400]}\"\"\"

Provide a plain-English explanation of exactly 3 bullet points (one sentence per bullet):
- Meaning: What this clause means in simple, practical terms.
- Risk Justification: Why this is flagged as a {risk_level} risk.
- Watch Out: One specific catch or detail the signing party must look out for.

Be concise and practical. No legal jargon."""

    try:
        active_client = _get_client()
        if not active_client:
            raise RuntimeError("GROQ_API_KEY not configured or groq package not available")

        model_name = os.getenv("GROQ_MODEL", "qwen/qwen3.6-27b")
        response = active_client.chat.completions.create(
            model=model_name,
            messages=[
                {
                    "role": "system",
                    "content": "You are a concise legal analyst. Always respond in 2-3 plain English sentences."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.6,
            max_completion_tokens=2048,
            top_p=0.95,
            reasoning_effort="default"
        )
        explanation = response.choices[0].message.content.strip()
        explanation = re.sub(r"<think>.*?</think>", "", explanation, flags=re.DOTALL)
        if "<think>" in explanation:
            explanation = explanation.split("<think>")[0]
        explanation = explanation.strip()
        if not explanation:
            explanation = (
                f"Clause flagged as {risk_level} RISK.\n"
                f"Reason: {risk_reason}"
            )

    except Exception as e:
        print(f"[explainability] Groq API call failed: {e}")
        explanation = (
            f"Clause flagged as {risk_level} RISK.\n"
            f"Reason: {risk_reason}"
        )

    risk_analysis["explanation"] = explanation
    return risk_analysis
