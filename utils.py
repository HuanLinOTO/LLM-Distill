import json
import os


if not os.path.exists("data"):
    os.makedirs("data")


def gradio_history_to_list(history):
    result = []
    for message in history:
        result.append(
            {
                "role": "user",
                "content": message[0],
            },
        )
        if len(message) > 1:
            result.append(
                {
                    "role": "assistant",
                    "content": message[1],
                },
            )
    return result


def list_to_gradio_history(history):
    result = []
    for i in range(0, len(history), 2):
        result.append(
            (
                history[i]["content"],
                history[i + 1]["content"],
            ),
        )
    return result


def save_conversation(history, id):
    with open(f"data/{id}.json", "w", encoding="utf-8") as f:
        json.dump(
            {"conversation": gradio_history_to_list(history)},
            f,
            ensure_ascii=False,
            indent=4,
        )
