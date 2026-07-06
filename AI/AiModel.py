import os
import requests
import json
from dotenv import load_dotenv
load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")
if not API_KEY:
    raise SystemExit("OPENROUTER_API_KEY is not set")

# First API call with reasoning
try:
    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
        },
        timeout=30,
        data=json.dumps({
            "model": "tencent/hy3:free",
            "messages": [
                {
                    "role": "user",
                    "content": "How many r's are in the word 'strawberry'?"
                }
            ],
            "reasoning": {"enabled": True}
        })
    )
except requests.RequestException as exc:
    raise SystemExit(f"API request failed: {exc}")

try:
    response.raise_for_status()
except requests.RequestException as exc:
    raise SystemExit(f"API request failed: {exc}")

try:
    response = response.json()
except ValueError as exc:
    raise SystemExit(f"Invalid JSON response: {exc}")

print(response)
choices = response.get("choices")
if not isinstance(choices, list) or not choices:
    raise SystemExit("No choices returned from API")

message = choices[0].get("message")
if not isinstance(message, dict):
    raise SystemExit("No message object found in API response")

# Preserve the assistant message with reasoning_details
messages = [
  {"role": "user", "content": "How many r's are in the word 'strawberry'?"},
  {
    "role": "assistant",
    "content": message.get('content'),
    "reasoning_details": message.get('reasoning_details')
  },
  {"role": "user", "content": "Are you sure? Think carefully."}
]

# Second API call - model continues reasoning from where it left off
try:
    response2 = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
        },
        timeout=30,
        data=json.dumps({
            "model": "tencent/hy3:free",
            "messages": messages,
            "reasoning": {"enabled": True}
        })
    )
    response2.raise_for_status()
except requests.RequestException as exc:
    raise SystemExit(f"API request failed: {exc}")

try:
    print(response2.json())
except ValueError as exc:
    raise SystemExit(f"Invalid JSON response from second request: {exc}")