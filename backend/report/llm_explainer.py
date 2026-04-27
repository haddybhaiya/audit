import os
import requests


def generate_llm_explanation(metrics):

    prompt = f"""
You are an AI fairness auditor.

Interpret the fairness metrics correctly.

Rules:
- Disparate Impact near 1.0 means fair
- Disparate Impact below 0.8 indicates bias
- Counterfactual Difference near 0 means fair
- Higher Protected Feature Importance means model relies on protected attribute

Metrics:
Disparate Impact: {metrics['disparate_impact']}
Counterfactual Difference: {metrics['counterfactual_difference']}
Protected Feature Importance: {metrics['protected_importance']}

Explain:
1. Is the model biased
2. Why it is biased
3. Which feature causes bias
4. Severity
Keep explanation concise.
"""

    api_key = os.getenv("GROQ_API_KEY")

    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    body = {
        "model": "llama-3.1-8b-instant",
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.2
    }

    response = requests.post(url, headers=headers, json=body)
    data = response.json()

    if "choices" not in data:
        return f"LLM explanation unavailable: {data}"

    return data["choices"][0]["message"]["content"]