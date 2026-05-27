from abc import ABC, abstractmethod
from typing import Optional
from langchain_core.embeddings import Embeddings
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import HumanMessage, AIMessage
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_openai import ChatOpenAI
from p5Agent.utils.config_handler import rag_config


class MockChatModel(BaseChatModel):
    def _generate(self, messages, stop=None, run_manager=None, **kwargs):
        from langchain_core.outputs import ChatResult, ChatGeneration
        
        last_message = messages[-1]
        if isinstance(last_message, HumanMessage):
            response = f"模拟回复：您问的是 '{last_message.content}'。这是一个模拟的 AI 响应。"
        else:
            response = "这是一个模拟的 AI 响应。"
        
        return ChatResult(
            generations=[ChatGeneration(message=AIMessage(content=response))]
        )

    @property
    def _llm_type(self):
        return "mock"


class MockEmbeddings(Embeddings):
    def embed_documents(self, texts):
        return [[0.1] * 384 for _ in texts]
    
    def embed_query(self, text):
        return [0.1] * 384


class BaseModelFactory(ABC):
    @abstractmethod
    def generator(self) -> Optional[Embeddings | BaseChatModel]:
        pass


class ChatModelFactory(BaseModelFactory):
    def generator(self) -> Optional[BaseChatModel]:
        try:
            return ChatOpenAI(
                model=rag_config["chat_model_name"],
                base_url=rag_config["base_url"],
            )
        except Exception as e:
            print(f"警告：无法创建真实模型，使用模拟模型: {e}")
            return MockChatModel()


class EmbeddingsFactory(BaseModelFactory):
    def generator(self) -> Optional[Embeddings]:
        try:
            return DashScopeEmbeddings(
                model_name=rag_config["embedding_model_name"],
            )
        except Exception as e:
            print(f"警告：无法创建真实嵌入模型，使用模拟模型: {e}")
            return MockEmbeddings()


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
