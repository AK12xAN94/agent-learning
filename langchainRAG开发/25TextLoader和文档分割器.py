from langchain_community.document_loaders import TextLoader
import os
from langchain_community.text_splitters import RecursiveCharacterTextSplitter

current_dir = os.path.dirname(os.path.abspath(__file__))
txt_path = os.path.join(current_dir, "data", "stu.txt")

loader = TextLoader(
    file_path=txt_path,
    encoding="utf-8")
docs = loader.load()
for doc in docs:
    print(type(doc), doc.page_content)

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500, # 分段的最大字符数
    chunk_overlap=50, # 分段之间允许重叠的字符数
    # 文本自然段落分隔的依据符号
    separators=["\n\n", "\n", " ", ""],
    length_function=len, # 分段的长度函数，默认是len
    keep_separator=True, # 是否保留分隔符，默认True
)
split_docs = splitter.split_documents(docs)
for doc in split_docs:
    print(doc.page_content)