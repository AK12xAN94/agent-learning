import warnings
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core._api.deprecation import (
    LangChainDeprecationWarning,
    LangChainPendingDeprecationWarning,
)

warnings.filterwarnings("ignore", category=LangChainDeprecationWarning)
warnings.filterwarnings("ignore", category=LangChainPendingDeprecationWarning)



@tool(description="查询天气")
def get_weather():
    """获取指定城市的天气"""
    return "晴天"


agent = create_agent(
    model=ChatOpenAI(
        model="qwen3.6-plus",
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    ),
    tools=[get_weather],
    system_prompt="你是一个智能聊天助手.",
)

res = agent.invoke({"messages": [{"role": "user", "content": "今天广州天气如何"}]})

for message in res["messages"]:
    print(message.type, message.content)
