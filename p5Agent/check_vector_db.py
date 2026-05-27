"""
查看向量数据库中的所有数据
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from langchain_chroma import Chroma
from langchain_core.embeddings import Embeddings
from p5Agent.utils.config_handler import chroma_config
from p5Agent.utils.path_tool import get_abs_path


class MockEmbeddings(Embeddings):
    def embed_documents(self, texts):
        return [[0.1] * 384 for _ in texts]

    def embed_query(self, text):
        return [0.1] * 384


def check_vector_db():
    # 获取持久化目录的绝对路径
    persist_dir = get_abs_path(chroma_config["persist_directory"])
    print(f"使用的向量数据库路径: {persist_dir}")

    # 初始化向量存储
    embedding_func = MockEmbeddings()
    vector_store = Chroma(
        collection_name=chroma_config["collection_name"],
        embedding_function=embedding_func,
        persist_directory=persist_dir,
    )

    # 获取所有文档
    try:
        # 使用 get() 方法获取所有文档
        all_docs = vector_store.get()

        if not all_docs or len(all_docs.get("ids", [])) == 0:
            print("向量数据库为空")
            return

        print(f"=== 向量数据库统计信息 ===")
        print(f"文档总数: {len(all_docs['ids'])}")
        print(f"持久化目录: {chroma_config['persist_directory']}")
        print(f"集合名称: {chroma_config['collection_name']}")
        print()

        print(f"=== 文档详情 ===")
        for i, (doc_id, content, metadata) in enumerate(
            zip(
                all_docs["ids"],
                all_docs["documents"],
                all_docs.get("metadatas", [{}] * len(all_docs["ids"])),
            ),
            1,
        ):
            print(f"\n--- 文档 {i} ---")
            print(f"ID: {doc_id}")
            print(f"来源: {metadata.get('source', '未知')}")
            print(f"类型: {metadata.get('type', '未知')}")
            print(f"内容预览:")
            if len(content) > 200:
                print(f"  {content[:200]}...")
            else:
                print(f"  {content}")

    except Exception as e:
        print(f"查询向量数据库失败: {str(e)}")


if __name__ == "__main__":
    check_vector_db()
