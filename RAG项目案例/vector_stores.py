import config_data as config
from langchain_chroma import Chroma


class VectorStoreService(object):
    """
    向量存储类
    """

    def __init__(self, embedding):
        self.embedding = embedding

        self.vector_store = Chroma(
            collection_name=config.collection_name,  # 数据库的表名
            embedding_function=self.embedding,
            persist_directory=config.persist_directory,
        )

    def get_retriever(self):
        return self.vector_store.as_retriever(
            search_kwargs={"k": config.similarity_threshold}
        )

if __name__ == "__main__":
    from langchain_community.embeddings import DashScopeEmbeddings
    embedding = DashScopeEmbeddings(model="text-embedding-v3")
    vector_store_service = VectorStoreService(embedding)
    retriever = vector_store_service.get_retriever()
    results = retriever.invoke("我的体重180斤，尺码推荐")
    print(results)
