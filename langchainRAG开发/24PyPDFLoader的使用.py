from langchain_community.document_loaders import PyPDFLoader
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
pdf_path = os.path.join(current_dir, "data", "stu.pdf")

loader = PyPDFLoader(
    file_path=pdf_path,
    encoding="utf-8",
)
docs = loader.lazy_load()
for doc in docs:
    print(doc.page_content)
