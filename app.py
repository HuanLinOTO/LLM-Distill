import random
import string
import gradio as gr

from backends.ollama import run_llm
from utils import save_conversation


demo = gr.Blocks()

CHARACTER_NAME = "纳西妲"


# 随机生成一个 uuid
def get_id():
    return "".join(
        random.choices(
            string.ascii_letters + string.digits,
            k=64,
        )
    )


def generate_response(msg, history, id):
    if "猫娘" in msg:
        gr.Info("不准猫娘！")
        yield "", []
    else:
        print(history, msg)
        # history.append(gr.ChatMessage(role="user", content=msg))

        result = ""
        for llm_output in run_llm(msg, history):
            result = llm_output
            output = (
                msg,
                result,
            )

            yield "", history + [output]

        history.append(output)
        save_conversation(history, id)
        yield "", history


with demo:
    id = gr.Textbox(
        get_id,
        visible=False,
    )
    chatbot = gr.Chatbot(
        label="对话框",
    )
    msg = gr.Textbox(
        label="有什么问题想问" + CHARACTER_NAME + "吗？",
        interactive=True,
        autofocus=True,
    )
    with gr.Row():
        submit = gr.Button("提交", variant="primary")
        clear = gr.ClearButton([msg, chatbot], value="清除")

    msg.submit(generate_response, inputs=[msg, chatbot, id], outputs=[msg, chatbot])
    submit.click(generate_response, inputs=[msg, chatbot, id], outputs=[msg, chatbot])

    clear.click(get_id, outputs=[id])

demo.launch()
