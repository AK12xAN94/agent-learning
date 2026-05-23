from langchain_openai import ChatOpenAI

# 使用 OpenAI 兼容模式访问通义千问，支持流式输出
model = ChatOpenAI(
    model="qwen3.6-plus",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    api_key="sk-18f59fad818846f3b74f24a08863731a",
    streaming=True
)

res = model.stream("烈咬陆鲨的种族值是多少")
for chunk in res:
    print(chunk.content, end="", flush=True)