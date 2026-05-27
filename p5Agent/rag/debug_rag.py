"""
调试 RAG 检索效果 - 增强版
"""

import sys
import os

sys.path.insert(
    0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)

from p5Agent.rag.vector_store import VectorStoreService


def debug_rag_retrieval(query: str, k: int = 10):
    print(f"=== 检索查询：{query} ===")
    print(f"检索数量：{k}\n")

    vector_store = VectorStoreService()
    retriever = vector_store.get_retriever(k=k)

    results = retriever.invoke(query)

    print(f"检索到 {len(results)} 条结果\n")

    # 按类型分组统计
    knowledge_count = 0
    prompt_count = 0

    for i, doc in enumerate(results, 1):
        doc_type = doc.metadata.get("type", "未知")
        source = doc.metadata.get("source", "未知")

        if doc_type == "knowledge":
            knowledge_count += 1
        elif doc_type == "prompt":
            prompt_count += 1

        print(f"--- 结果 {i} ---")
        print(f"来源：{source}")
        print(f"类型：{doc_type}")
        print(f"内容预览：{doc.page_content[:150]}...\n")

    print(f"\n=== 统计 ===")
    print(f"知识库文档：{knowledge_count} 条")
    print(f"提示词文档：{prompt_count} 条")

    if knowledge_count == 0:
        print("\n⚠️  未检索到知识库内容，建议：")
        print("1. 检查知识库文档是否已正确加载")
        print("2. 增加检索数量 k 值")
        print("3. 优化查询关键词")


if __name__ == "__main__":
    query = "小户型适合哪些扫地机器人"
    debug_rag_retrieval(query, k=10)
