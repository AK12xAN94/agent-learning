"""
知识库
"""

import os
import config_data as config
import hashlib
from langchain_chroma import Chroma
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from datetime import datetime


def check_md5(md5_str):
    """
    检查传入的md5字符串是否已经被处理过了
    """
    if not os.path.exists(config.md5_path):
        # 不存在，肯定没有处理过
        open(config.md5_path, "w", encoding="utf-8").close()  # create file if not exist
        return False
    else:
        for line in open(config.md5_path, "r", encoding="utf-8").readlines():
            if line.strip() == md5_str:
                return True
        return False


def save_md5(md5_str):
    """
    保存传入的md5字符串
    """
    with open(config.md5_path, "a", encoding="utf-8") as f:
        f.write(md5_str + "\n")


def get_string_md5(input_str, encoding="utf-8"):
    """
    获取传入的字符串的md5值
    """
    import hashlib

    return hashlib.md5(
        input_str.encode(encoding)
    ).hexdigest()  # 返回hashlib.md5方法处理过的十六进制字符串


class KnowledgeBaseService(object):
    """
    知识库类
    """

    def __init__(self):
        # 如果文件夹不存在则创建，否则跳过
        os.makedirs(config.persist_directory, exist_ok=True)
        # 向量存储的实例 Chroma向量库对象
        self.chroma = Chroma(
            collection_name=config.collection_name,  # 数据库的表名
            embedding_function=DashScopeEmbeddings(
                model="text-embedding-v3",
                dashscope_api_key="sk-18f59fad818846f3b74f24a08863731a",
            ),
            persist_directory=config.persist_directory,  # 数据库的存储路径
        )
        # 文本分割器对象
        self.spliter = RecursiveCharacterTextSplitter(
            chunk_size=config.chunk_size,  # 每个文本块的大小
            chunk_overlap=config.chunk_overlap,  # 每个文本块之间的重叠大小
            separators=config.separators,  # 文本块的分隔符
            length_function=len,  # 递归分割器的长度函数，用于计算文本块的长度
        )

    def upload_by_str(self, data: str, filename):
        """
        把传入的字符串，进行向量化，存入向量数据库中
        """
        md5_hex = get_string_md5(data)

        if check_md5(md5_hex):
            # 已经处理过了，直接返回
            return "[跳过]内容已经存在知识库中"

        if len(data) > config.max_split_char_number:
            knowledge_chunks: list[str] = self.spliter.split_text(data)

        else:
            knowledge_chunks: list[str] = [data]

        meta_data = {
            "source": filename,
            "create_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "operation": "user",
        }

        # 存储向量到向量数据库中
        self.chroma.add_texts(
            knowledge_chunks, metadatas=[meta_data for _ in knowledge_chunks]
        )
        save_md5(md5_hex)  # 保存md5值到文件

        return "[成功]内容已添加到向量库"


if __name__ == "__main__":
    service = KnowledgeBaseService()
    print(service.upload_by_str("你好", "test.txt"))
