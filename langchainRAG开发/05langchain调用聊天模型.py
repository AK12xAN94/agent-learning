from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

# 使用 OpenAI 兼容模式访问通义千问聊天模型
model = ChatOpenAI(
    model="qwen3.6-plus",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    api_key="sk-18f59fad818846f3b74f24a08863731a",
    streaming=True
)

messages = [
    SystemMessage(content="你是一个专业的宝可梦对战大师，话很多。"),
    HumanMessage(content="最强的mega宝可梦是哪个"),
]

res = model.stream(messages)
for chunk in res:
    print(chunk.content, end="", flush=True)