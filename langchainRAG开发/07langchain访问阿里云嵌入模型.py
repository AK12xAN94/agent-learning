from langchain_community.embeddings import DashScopeEmbeddings

# 使用 DashScope 访问阿里云嵌入模型
model = DashScopeEmbeddings(
    model="text-embedding-v3",  # 阿里云嵌入模型名称
    dashscope_api_key="sk-18f59fad818846f3b74f24a08863731a"
)

print(model.embed_query("我喜欢你"))
print(model.embed_documents(["我喜欢你"]))