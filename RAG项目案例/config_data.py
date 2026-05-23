import os

# 获取当前脚本所在目录
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

md5_path = os.path.join(BASE_DIR, "md5.txt")

DASHSCOPE_API_KEY = "sk-18f59fad818846f3b74f24a08863731a"

# Chroma
collection_name = "rag"
persist_directory = os.path.join(BASE_DIR, "chroma_db")

# splitter
chunk_size = 1000
chunk_overlap = 100
separators = ["\n\n", "\n", " ", "", "?", "？", ".", "。"]
max_split_char_number = 1000

# vector store
similarity_threshold = 1  # 检索返回匹配的文档数量

# rag
embedding_model_name = "text-embedding-v3"
chat_model_name = "qwen3.6-plus"

session_config = {"configurable": {"session_id": "user_001"}}
