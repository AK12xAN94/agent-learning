from langchain_chroma import Chroma
from p5Agent.utils.path_tool import get_abs_path
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.embeddings import Embeddings
import os


class MockEmbeddings(Embeddings):
    def embed_documents(self, texts):
        return [[0.1] * 384 for _ in texts]
    
    def embed_query(self, text):
        return [0.1] * 384


class VectorStoreService:
    def __init__(self):
        self.vector_store = Chroma(
            collection_name="test_agent",
            embedding_function=MockEmbeddings(),
            persist_directory="./chroma_db_test",
        )

        self.spliter = RecursiveCharacterTextSplitter(
            chunk_size=200,
            chunk_overlap=20,
            length_function=len,
        )

    def get_retriever(self):
        retriever = self.vector_store.as_retriever(
            search_kwargs={"k": 3},
        )
        return retriever

    def load_document(self, content):
        documents = [Document(page_content=content, metadata={"source": "test"})]
        split_documents = self.spliter.split_documents(documents)
        self.vector_store.add_documents(split_documents)
        print(f"已加载 {len(split_documents)} 个文档片段")


if __name__ == "__main__":
    print("=== 测试向量存储服务 ===")
    
    vector_store_service = VectorStoreService()
    print("VectorStoreService 初始化成功")
    
    test_content = """
    迷路怎么办？
    如果在户外迷路，首先不要惊慌。可以尝试以下方法：
    1. 保持冷静，不要乱走
    2. 寻找明显的地标
    3. 使用指南针或手机导航
    4. 如果有地图，查看地图确定位置
    5. 必要时拨打求救电话
    """
    
    vector_store_service.load_document(test_content)
    print("文档加载成功")
    
    retriever = vector_store_service.get_retriever()
    print("检索器创建成功")
    
    results = retriever.invoke("迷路")
    print(f"\n=== 检索结果 (共 {len(results)} 条) ===")
    for i, result in enumerate(results):
        print(f"\n结果 {i+1}:")
        print(result.page_content)
