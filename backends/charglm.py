from transformers import AutoTokenizer, AutoModel

from utils import gradio_history_to_list

tokenizer = AutoTokenizer.from_pretrained(
    "thu-coai/CharacterGLM-6B", trust_remote_code=True
)
model = AutoModel.from_pretrained(
    "thu-coai/CharacterGLM-6B", trust_remote_code=True, device="cuda"
)
model = model.eval()

session_meta = {
    "bot_name": "纳西妲",
    "bot_info": open("charglm_prompt.txt", encoding="utf-8").read(),
    "user_name": "旅行者",
    "user_info": "我叫旅行者，性别未知，纳西妲和我是在须弥城认识的。纳西妲是须弥的草神，我前往须弥寻找关于自己失踪兄妹的信息。在此过程中，我得知了须弥城中有一位神秘的草神，即纳西妲。纳西妲一直被关在须弥的大图书馆中，我通过一系列的任务和探索，最终找到了纳西妲，并与她建立了联系。纳西妲在见到我后，逐渐信任我，并与他一起揭开了关于须弥的一系列秘密，共同面对各种挑战。",
}

# response, history = model.chat(tokenizer, session_meta, "你好", history=[])


def run_llm(msg, history):
    for response, history in model.stream_chat(
        tokenizer=tokenizer,
        session_meta=session_meta,
        query=msg,
        history=gradio_history_to_list(history),
        top_p=1,
        temperature=0.01,
        past_key_values=None,
    ):
        yield response, history
