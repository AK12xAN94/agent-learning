# import os
from langchain_openai import ChatOpenAI

# 配置阿里云百炼 API Key
# os.environ["OPENAI_API_KEY"] = "sk-18f59fad818846f3b74f24a08863731a"

# 使用 OpenAI 兼容模式访问通义千问
model = ChatOpenAI(
    model="qwen3.6-plus",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    # api_key="sk-18f59fad818846f3b74f24a08863731a"
)

response = model.invoke("烈咬陆鲨的种族值是多少")
print(response.content)