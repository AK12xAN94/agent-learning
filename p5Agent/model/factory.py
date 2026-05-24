from abc import ABC, abstractmethod
from typing import Optional
from langchain_community.embeddings import Embeddings
from langchain_community.chat_models import BaseChatModel
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_chatOpenAI import ChatOpenAI
from utils.config_handler import rag_config

class BaseModelFactory(ABC):
    @abstractmethod
    def generator(self) -> Optional[Embeddings | BaseChatModel]:
        pass

class ChatModelFactory(BaseModelFactory):
    def generator(self) -> Optional[BaseChatModel]:
        return ChatOpenAI(
            model_name=rag_config["model_name"],
            base_url=rag_config["base_url"],
        )

class EmbeddingsFactory(BaseModelFactory):
    def generator(self) -> Optional[Embeddings]:
        return DashScopeEmbeddings(
            model_name=rag_config["embedding_model_name"],
        )


chat_model = ChatModelFactory().generator()
embed_model = EmbeddingsFactory().generator()
