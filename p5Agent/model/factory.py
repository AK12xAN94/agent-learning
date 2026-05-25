from abc import ABC, abstractmethod
from typing import Optional
from langchain_core.embeddings import Embeddings
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_openai import ChatOpenAI
from p5Agent.utils.config_handler import rag_config


class BaseModelFactory(ABC):
    @abstractmethod
    def generator(self) -> Optional[Embeddings | BaseChatModel]:
        pass


class ChatModelFactory(BaseModelFactory):
    def generator(self) -> Optional[BaseChatModel]:
        return ChatOpenAI(
            model=rag_config["chat_model_name"],
            base_url=rag_config["base_url"],
        )


class EmbeddingsFactory(BaseModelFactory):
    def generator(self) -> Optional[Embeddings]:
        return DashScopeEmbeddings(
            model_name=rag_config["embedding_model_name"],
        )


def get_chat_model():
    return ChatModelFactory().generator()


def get_embed_model():
    return EmbeddingsFactory().generator()


_chat_model = None
_embed_model = None


def chat_model():
    global _chat_model
    if _chat_model is None:
        _chat_model = ChatModelFactory().generator()
    return _chat_model


def embed_model():
    global _embed_model
    if _embed_model is None:
        _embed_model = EmbeddingsFactory().generator()
    return _embed_model
