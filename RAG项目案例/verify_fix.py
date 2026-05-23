"""
验证修复后的配置路径
"""
import os
import sys

print("=" * 60)
print("✅ 验证修复后的配置路径")
print("=" * 60)

# 重新加载 config_data
if 'config_data' in sys.modules:
    del sys.modules['config_data']

import config_data

print(f"\n1. BASE_DIR: {config_data.BASE_DIR}")
print(f"\n2. md5_path: {config_data.md5_path}")
print(f"   md5.txt 存在: {os.path.exists(config_data.md5_path)}")

print(f"\n3. persist_directory: {config_data.persist_directory}")
print(f"   chroma_db 存在: {os.path.exists(config_data.persist_directory)}")

# 验证向量库
print(f"\n4. 验证向量库中的数据:")
from langchain_chroma import Chroma
from langchain_community.embeddings import DashScopeEmbeddings

embeddings = DashScopeEmbeddings(
    model="text-embedding-v3",
    dashscope_api_key=config_data.DASHSCOPE_API_KEY
)

vector_store = Chroma(
    collection_name=config_data.collection_name,
    embedding_function=embeddings,
    persist_directory=config_data.persist_directory,
)

results = vector_store.get()
print(f"   向量库文档数: {len(results['documents'])}")

for i, doc in enumerate(results['documents']):
    source = results['metadatas'][i].get('source', 'N/A')
    print(f"   文档 {i+1}: {source}")

print("\n" + "=" * 60)
print("💡 现在所有数据都存储在脚本目录下了！")
print("=" * 60)