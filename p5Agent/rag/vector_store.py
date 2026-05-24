from langchain_chroma import Chroma
from utils.config_handler import chroma_config
from model.factory import embed_model
from langchain_community.text_splitters import RecursiveCharacterTextSplitter



class VectorStoreService:
    def __init__(self):
        self.vector_store = Chroma(
            collection_name=chroma_config["collection_name"],
            embedding_function=embed_model,
            persist_directory=chroma_config["persist_directory"],
        )

        self.spliter = RecursiveCharacterTextSplitter(
            chunk_size=chroma_config["chunk_size"],
            chunk_overlap=chroma_config["chunk_overlap"],
        )
