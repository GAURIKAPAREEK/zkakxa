import requests
import json


def generate_anomaly_explanation(anomaly_summary: dict, api_key: str) -> str:
    """
    Claude API ko call karke ek detected anomaly ka human-readable explanation
    generate karta hai — jaise ek data engineer khud likhta.
    """
    prompt = f"""You are a data quality expert. Based on this anomaly detection summary, 
write a SHORT (2-3 sentences) explanation of what likely went wrong and a suggested action.
Be specific and professional, like an alert message a data engineer would read.

Anomaly Data:
{json.dumps(anomaly_summary, indent=2)}

Respond with ONLY the explanation text, no preamble."""

    try:
        response = requests.post(
            "https://api.anthropic.com/v1/messages",
            headers={
                "Content-Type": "application/json",
                "x-api-key": api_key,
                "anthropic-version": "2023-06-01"
            },
            json={
                "model": "claude-sonnet-4-6",
                "max_tokens": 200,
                "messages": [{"role": "user", "content": prompt}]
            }
        )
        data = response.json()
        explanation = data["content"][0]["text"]
        return explanation.strip()

    except Exception as e:
        return f"AI explanation unavailable: {str(e)}"