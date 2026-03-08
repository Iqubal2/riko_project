# OpenAI tool calling with history
import copy
import json
import os

import yaml
from openai import OpenAI

with open('character_config.yaml', 'r') as f:
    char_config = yaml.safe_load(f)

client = OpenAI(api_key=char_config['OPENAI_API_KEY'])

# Constants
HISTORY_FILE = char_config['history_file']
MODEL = char_config['model']
SYSTEM_PROMPT = [
    {
        "role": "system",
        "content": [
            {
                "type": "input_text",
                "text": char_config['presets']['default']['system_prompt']
            }
        ]
    }
]


def _fresh_system_prompt():
    return copy.deepcopy(SYSTEM_PROMPT)


# Load/save chat history
def load_history():
    if not os.path.exists(HISTORY_FILE):
        return _fresh_system_prompt()

    try:
        with open(HISTORY_FILE, "r") as f:
            history = json.load(f)
    except (json.JSONDecodeError, OSError):
        return _fresh_system_prompt()

    if not isinstance(history, list) or not history:
        return _fresh_system_prompt()

    # Always keep the latest configured system prompt as the first message.
    if isinstance(history[0], dict) and history[0].get("role") == "system":
        history[0] = _fresh_system_prompt()[0]
        return history

    return _fresh_system_prompt() + history


def save_history(history):
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=2)


def get_riko_response_no_tool(messages):
    # Call OpenAI with system prompt + history
    response = client.responses.create(
        model=MODEL,
        input=messages,
        temperature=1,
        top_p=1,
        max_output_tokens=2048,
        stream=False,
        text={
            "format": {
                "type": "text"
            }
        },
    )

    return response


def llm_response(user_input):
    messages = load_history()

    # Append user message to memory
    messages.append({
        "role": "user",
        "content": [
            {"type": "input_text", "text": user_input}
        ]
    })

    riko_test_response = get_riko_response_no_tool(messages)

    # Append assistant message to regular response
    messages.append({
        "role": "assistant",
        "content": [
            {"type": "output_text", "text": riko_test_response.output_text}
        ]
    })

    save_history(messages)
    return riko_test_response.output_text


if __name__ == "__main__":
    print('running main')
