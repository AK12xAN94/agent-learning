from vector_stores import VectorStoreService
from langchain_community.embeddings import DashScopeEmbeddings
import config_data as config
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from file_history_store import get_history


class RagService(object):
    """
    RAG服务类
    """

    def __init__(self):
        self.embeddings = DashScopeEmbeddings(
            model=config.embedding_model_name,
            dashscope_api_key=config.DASHSCOPE_API_KEY,
        )
        self.vector_service = VectorStoreService(embedding=self.embeddings)
        self.retriever = self.vector_service.get_retriever()
        self.chat_model = ChatOpenAI(
            model_name=config.chat_model_name,
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
            api_key=config.DASHSCOPE_API_KEY,
            streaming=True,
        )

    def chat(self, user_input, session_id="user_001"):
        """
        聊天接口（非流式）
        """
        # 获取历史消息
        history = get_history(session_id)
        history_messages = history.messages if hasattr(history, "messages") else []

        # 从向量库检索相关文档
        docs = self.retriever.invoke(user_input)

        # 格式化文档内容（转义花括号避免被当作模板变量）
        if not docs:
            context = "无相关参考资料"
        else:
            context = ""
            for doc in docs:
                # 转义元数据中的花括号
                metadata_str = str(doc.metadata).replace("{", "{{").replace("}", "}}")
                context += (
                    f"文档片段：{doc.page_content}\n文档元数据：{metadata_str}\n\n"
                )

        # 构建消息列表
        messages = []
        messages.append(
            (
                "system",
                f"以我提供的已知参考资料为主，简洁和专业地回答用户问题，参考资料: {context}",
            )
        )

        # 添加历史消息
        if history_messages:
            for msg in history_messages:
                role = "human" if msg.type == "human" else "ai"
                messages.append((role, msg.content))

        # 添加当前用户输入
        messages.append(("human", user_input))

        # 创建提示模板并调用模型
        prompt = ChatPromptTemplate.from_messages(messages)
        result = self.chat_model.invoke(prompt.invoke({}).to_messages())

        # 保存历史消息
        history.add_user_message(user_input)
        history.add_ai_message(result.content)

        return result.content

    def chat_stream(self, user_input, session_id="user_001"):
        """
        聊天接口（流式输出）
        """
        # 获取历史消息
        history = get_history(session_id)
        history_messages = history.messages if hasattr(history, "messages") else []

        # 从向量库检索相关文档
        docs = self.retriever.invoke(user_input)

        # 格式化文档内容（转义花括号避免被当作模板变量）
        if not docs:
            context = "无相关参考资料"
        else:
            context = ""
            for doc in docs:
                # 转义元数据中的花括号
                metadata_str = str(doc.metadata).replace("{", "{{").replace("}", "}}")
                context += (
                    f"文档片段：{doc.page_content}\n文档元数据：{metadata_str}\n\n"
                )

        # 构建消息列表
        messages = []
        messages.append(
            (
                "system",
                f"以我提供的已知参考资料为主，简洁和专业地回答用户问题，参考资料: {context}",
            )
        )

        # 添加历史消息
        if history_messages:
            for msg in history_messages:
                role = "human" if msg.type == "human" else "ai"
                messages.append((role, msg.content))

        # 添加当前用户输入
        messages.append(("human", user_input))

        # 创建提示模板
        prompt = ChatPromptTemplate.from_messages(messages)

        # 保存用户消息到历史
        history.add_user_message(user_input)

        # 流式调用模型
        full_response = ""
        for chunk in self.chat_model.stream(prompt.invoke({}).to_messages()):
            if chunk.content:
                full_response += chunk.content
                yield chunk.content

        # 保存完整回复到历史
        history.add_ai_message(full_response)


if __name__ == "__main__":
    rag_service = RagService()
    result = rag_service.chat("我是一个男生，夏天应该怎么穿什么颜色")
    print(result)
