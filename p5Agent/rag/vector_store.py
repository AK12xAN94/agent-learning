import sys
import os

sys.path.insert(
    0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)

from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from p5Agent.utils.path_tool import get_abs_path
from p5Agent.utils.config_handler import chroma_config
import os


class MockEmbeddings(Embeddings):
    def embed_documents(self, texts):
        return [[0.1] * 384 for _ in texts]

    def embed_query(self, text):
        return [0.1] * 384


class VectorStoreService:
    def __init__(self, embedding_func=None):
        if embedding_func is None:
            embedding_func = MockEmbeddings()

        self.embedding_func = embedding_func
        self.vector_store = Chroma(
            collection_name=chroma_config["collection_name"],
            embedding_function=self.embedding_func,
            persist_directory=get_abs_path(chroma_config["persist_directory"]),
        )

        self.spliter = RecursiveCharacterTextSplitter(
            chunk_size=chroma_config["chunk_size"],
            chunk_overlap=chroma_config["chunk_overlap"],
            length_function=len,
        )

    def get_retriever(self, k: int = None):
        if k is None:
            k = chroma_config["k"]
        retriever = self.vector_store.as_retriever(
            search_kwargs={"k": k},
        )
        return retriever

    def load_document(self):
        data_dir = get_abs_path(chroma_config["data_path"])

        if not os.path.exists(data_dir):
            print(f"数据目录 {data_dir} 不存在，跳过加载")
            return

        md5_store_path = get_abs_path(chroma_config["md5_hex_store"])

        def check_md5_hex(md5_for_check):
            if not os.path.exists(md5_store_path):
                return False
            with open(md5_store_path, "r", encoding="utf-8") as f:
                lines = f.readlines()
                for line in lines:
                    if line.strip() == md5_for_check:
                        return True
            return False

        def save_md5_hex(md5_for_check):
            with open(md5_store_path, "a", encoding="utf-8") as f:
                f.write(md5_for_check + "\n")

        allow_file_types = chroma_config["allow_knowledge_file_type"]

        for filename in os.listdir(data_dir):
            if not any(filename.endswith(f".{ext}") for ext in allow_file_types):
                continue

            file_path = os.path.join(data_dir, filename)
            md5_hex = self._get_file_md5(file_path)

            if check_md5_hex(md5_hex):
                print(f"[加载知识库]{file_path}内容已存在知识库内，跳过")
                continue

            try:
                if filename.endswith(".txt"):
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()
                elif filename.endswith(".pdf"):
                    print(f"[加载知识库]PDF文件暂不支持，跳过: {file_path}")
                    continue
                else:
                    continue

                if not content.strip():
                    print(f"[加载知识库]{file_path}没有有效文本内容，跳过")
                    continue

                documents = [
                    Document(page_content=content, metadata={"source": filename})
                ]
                split_documents = self.spliter.split_documents(documents)

                if not split_documents:
                    print(f"[加载知识库]{file_path}分片后没有有效文本内容，跳过")
                    continue

                self.vector_store.add_documents(split_documents)
                save_md5_hex(md5_hex)
                print(f"[加载知识库]{file_path}内容已加载到向量库")
            except Exception as e:
                print(f"[加载知识库]{file_path}读取失败: {str(e)}")
                continue

    def _get_file_md5(self, file_path):
        import hashlib

        md5_obj = hashlib.md5()
        with open(file_path, "rb") as f:
            while chunk := f.read(4096):
                md5_obj.update(chunk)
        return md5_obj.hexdigest()


if __name__ == "__main__":
    print("=== 初始化向量存储服务 ===")
    vector_store_service = VectorStoreService()
    print("VectorStoreService 初始化成功")

    print("\n=== 加载文档 ===")
    vector_store_service.load_document()

    print("\n=== 创建检索器 ===")
    retriever = vector_store_service.get_retriever()
    print("检索器创建成功")

    print("\n=== 测试检索 ===")
    results = retriever.invoke("迷路")
    print(f"检索到 {len(results)} 条结果")
    for i, result in enumerate(results):
        print(f"\n结果 {i + 1}:")
        print(
            result.page_content[:200], "..." if len(result.page_content) > 200 else ""
        )
