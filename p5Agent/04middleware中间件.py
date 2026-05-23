import warnings
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core._api.deprecation import (
    LangChainDeprecationWarning,
    LangChainPendingDeprecationWarning,
)
from langchain.agents import before_agent, after_agent
from langchain.agents import AgentState
from langgraph.runtime import Runtime


warnings.filterwarnings("ignore", category=LangChainDeprecationWarning)
warnings.filterwarnings("ignore", category=LangChainPendingDeprecationWarning)



@tool(description="查询天气")
def get_weather():
    """获取指定城市的天气"""
    return "晴天"

"""
1. agent执行前
2. agent执行后
3. model执行前
4. model执行后
5. 工具执行中
6. 模型执行中不
"""



@before_agent
def log_before_agent(state: AgentState, runtime: Runtime):
    print(f"[before agent]agent启动，并附带{len(state.messages)}个消息")

@after_agent
def log_after_agent(state: AgentState, runtime: Runtime):
    print(f"[after agent]agent执行完成，共{len(state.messages)}个消息")
