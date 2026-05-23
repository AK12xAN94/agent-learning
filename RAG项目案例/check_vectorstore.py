"""
检查向量库中的数据
"""

from langchain_chroma import Chroma
from langchain_community.embeddings import DashScopeEmbeddings
import config_data as config

# 初始化嵌入模型
embeddings = DashScopeEmbeddings(
    model=config.embedding_model_name, dashscope_api_key=config.DASHSCOPE_API_KEY
)

# 连接向量库
vector_store = Chroma(
    collection_name=config.collection_name,
    embedding_function=embeddings,
    persist_directory=config.persist_directory,
)

# 获取所有数据
results = vector_store.get()

print(f"向量库中共有 {len(results['documents'])} 条文档\n")
print("=" * 50)

for i, doc in enumerate(results["documents"]):
    print(f"\n文档 {i + 1}:")
    print(f"内容: {doc[:200]}..." if len(doc) > 200 else doc)
    print(f"元数据: {results['metadatas'][i]}")

print("\n" + "=" * 50)

# 测试检索
test_query = "我体重200斤，身高180cm，应该买什么尺码"
print(f"\n测试检索 query: {test_query}")

docs_with_scores = vector_store.similarity_search_with_score(test_query, k=2)
for doc, score in docs_with_scores:
    print(f"\n相似度得分: {score}")
    print(f"文档内容: {doc.page_content[:200]}...")
