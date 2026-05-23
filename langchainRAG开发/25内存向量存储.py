from langchain_core.vectorstores import InMemoryVectorStore
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_community.document_loaders import CSVLoader
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(current_dir, "data", "info.csv")

embeddings = DashScopeEmbeddings(
    model="text-embedding-v3", dashscope_api_key="sk-18f59fad818846f3b74f24a08863731a"
)

loader = CSVLoader(
    file_path=csv_path,
    encoding="utf-8",
    source_column="source",  # 指定文档内容的列名
)
docs = loader.load()

vector_store = InMemoryVectorStore.from_documents(
    documents=docs, embedding=embeddings, ids=["id" + str(i) for i in range(len(docs))]
)

results = vector_store.similarity_search(
    query="Python是不是简单易学",
    k=1,
)
for result in results:
    print(result.page_content)
