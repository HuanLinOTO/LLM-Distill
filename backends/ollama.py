import ollama

from utils import gradio_history_to_list

system_prompt = open("./prompt.txt", encoding="utf-8").read()


def run_llm(msg, history):
    stream = ollama.chat(
        model="qwen2:7b-instruct",
        messages=[
            {"role": "system", "content": system_prompt},
            *gradio_history_to_list(history),
            {
                "role": "user",
                "content": msg,
            },
        ],
        stream=True,
        options={
            "temperature": 0.5,
        },
    )
    result = ""
    for chunk in stream:
        result += chunk["message"]["content"]
        yield result
