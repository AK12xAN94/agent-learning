"""
总结服务类：用户提问：搜索参考资料，将提问和参考资料提交给模型，让模型总结回复
"""

import sys
import os

sys.path.insert(
    0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)

from langchain_core.documents import Document

from p5Agent.utils.config_handler import rag_config
from p5Agent.rag.vector_store import VectorStoreService
from p5Agent.utils.prompts_loader import load_rag_prompts
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from p5Agent.model.factory import chat_model


class RagSummarizeService:
    def __init__(self):
        self.vector_store = VectorStoreService()
        self.retriever = self.vector_store.get_retriever()
        self.prompts_text = load_rag_prompts()
        self.prompt_template = PromptTemplate.from_template(self.prompts_text)
        self.model = chat_model()
        self.chain = self.init_chain()

    def init_chain(self):
        chain = self.prompt_template | self.model | StrOutputParser()
        return chain

    def retrieve_docs(self, query: str, k: int = 20) -> list[Document]:
        """
        搜索参考资料
        """
        retriever = self.vector_store.get_retriever(k=k)
        results = retriever.invoke(query)

        # 优先选择知识库文档
        knowledge_docs = [
            doc for doc in results if doc.metadata.get("type") == "knowledge"
        ]
        if knowledge_docs:
            return knowledge_docs[:3]  # 最多返回 3 条知识库文档

        # 如果没有知识库文档，返回所有结果
        return results[:3]

    def rag_summarize(self, query: str) -> str:
        context_docs = self.retrieve_docs(query)
        context = ""
        counter = 0
        for doc in context_docs:
            context += f"【参考资料{counter}】：参考资料：{doc.page_content} | 参考元数据：{doc.metadata}\n"
            counter += 1
        return self.chain.invoke({"input": query, "context": context})


if __name__ == "__main__":
    rag_config = RagSummarizeService()
    print(rag_config.rag_summarize("小户型适合哪些扫地机器人"))
