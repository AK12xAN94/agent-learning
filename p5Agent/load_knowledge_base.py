"""
加载知识库到向量数据库
支持 data 目录下的 txt 文件
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from p5Agent.utils.config_handler import chroma_config
from p5Agent.utils.path_tool import get_abs_path


class MockEmbeddings(Embeddings):
    def embed_documents(self, texts):
        return [[0.1] * 384 for _ in texts]
    
    def embed_query(self, text):
        return [0.1] * 384


def load_knowledge_base():
    # 获取持久化目录的绝对路径
    persist_dir = get_abs_path(chroma_config["persist_directory"])
    print(f"使用的向量数据库路径：{persist_dir}")
    
    # 初始化向量存储
    embedding_func = MockEmbeddings()
    vector_store = Chroma(
        collection_name=chroma_config["collection_name"],
        embedding_function=embedding_func,
        persist_directory=persist_dir,
    )

    spliter = RecursiveCharacterTextSplitter(
        chunk_size=chroma_config["chunk_size"],
        chunk_overlap=chroma_config["chunk_overlap"],
        length_function=len,
    )

    # data 目录路径
    data_dir = get_abs_path(chroma_config["data_path"])
    
    if not os.path.exists(data_dir):
        print(f"知识库目录 {data_dir} 不存在")
        return

    print(f"\n=== 开始加载知识库 ===")
    print(f"知识库目录：{data_dir}\n")

    # 遍历 data 目录下的所有 txt 文件
    for filename in os.listdir(data_dir):
        if not filename.endswith(".txt"):
            continue
        
        file_path = os.path.join(data_dir, filename)
        
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            
            if not content.strip():
                print(f"[跳过]{filename} - 文件为空")
                continue
            
            # 创建文档对象
            documents = [Document(
                page_content=content, 
                metadata={"source": filename, "type": "knowledge"}
            )]
            
            # 分片处理
            split_documents = spliter.split_documents(documents)
            
            if not split_documents:
                print(f"[跳过]{filename} - 分片后为空")
                continue
            
            # 添加到向量数据库
            vector_store.add_documents(split_documents)
            print(f"[成功]{filename} - 已存入向量数据库（{len(split_documents)}个片段）")
            
        except Exception as e:
            print(f"[失败]{filename} - {str(e)}")
    
    print("\n=== 知识库加载完成 ===")


if __name__ == "__main__":
    load_knowledge_base()
