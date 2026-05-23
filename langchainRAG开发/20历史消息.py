from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableWithMessageHistory


def print_prompt(full_prompt: str):
    print("=" * 20, full_prompt.tostring(), "=" * 20)
    return full_prompt


model = ChatOpenAI(
    model="qwen3.6-plus",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    api_key="sk-18f59fad818846f3b74f24a08863731a",
    streaming=True,
)

prompt = PromptTemplate.from_template(
    "你需要根据对话历史回应用户问题。对话历史: {chat_history}。用户当前输入: {input}，请给出回应"
)

str_parser = StrOutputParser()

base_chain = prompt | print_prompt | model | str_parser

store = {} #key: session_id, value: chat_history
def get_history(session_id):
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]


conversation_chain = RunnableWithMessageHistory(
    base_chain, 
    get_history, 
    input_messages_key='input',
    history_key='chat_history',
)

if __name__ == '__main__':
    session_config = {
        'configurable' : {
            'session_id': 'user_001'
        }
    }
    res = conversation_chain.invoke({'input': '小明有两只猫'}, session_config)
    print('第一次对话',res)

    res = conversation_chain.invoke({'input': '小刚有一只狗'}, session_config)
    print('第二次对话',res)

    res = conversation_chain.invoke({'input': '请问总共有多少只宠物'}, session_config)
    print('第三次对话',res)

