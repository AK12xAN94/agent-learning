from langchain_openai import ChatOpenAI

model = ChatOpenAI(
    model="qwen3.6-plus",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    api_key="sk-18f59fad818846f3b74f24a08863731a",
    streaming=True
)

messages = [
    ('system', '你是一个专业的宝可梦对战大师，话很多。'),
    ('assistant', '好的，我是一个专业的宝可梦对战大师，我可以回答你关于宝可梦对战的问题。'),
    ('user', '最强的mega宝可梦是哪个'),
]

res = model.stream(messages)
for chunk in res:
    print(chunk.content, end="", flush=True)