from langchain_ollama import OllamaLLM

# 使用 Ollama 访问本地模型
model = OllamaLLM(
    model="deepseek-r1:7b"  # 模型名称，Ollama 会自动连接本地服务
)

response = model.invoke("烈咬陆鲨的种族值是多少")
print(response)