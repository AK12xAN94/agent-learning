import warnings
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
from langchain_core._api.deprecation import (
    LangChainDeprecationWarning,
    LangChainPendingDeprecationWarning,
)


warnings.filterwarnings("ignore", category=LangChainDeprecationWarning)
warnings.filterwarnings("ignore", category=LangChainPendingDeprecationWarning)


@tool(description="查询指定城市的天气，参数为city，返回值为天气")
def get_weather(city: str):
    """获取指定城市的天气"""
    return f"{city}的天气是晴天"


def log_before_agent(state):
    messages = state.get("messages", [])
    print(f"[before agent]agent启动，并附带{len(messages)}个消息")
    return state


def log_after_agent(state):
    messages = state.get("messages", [])
    print(f"[after agent]agent执行完成，共{len(messages)}个消息")
    return state


def log_before_model(state):
    messages = state.get("messages", [])
    print(f"[before model]model启动，并附带{len(messages)}个消息")
    return state


def log_after_model(state):
    messages = state.get("messages", [])
    print(f"[after model]model执行完成，共{len(messages)}个消息")
    return state


def model_call_hook(state):
    print(f"[model call hook]准备调用模型")
    return state


def monitor_tool(state):
    last_message = state.get("messages", [])[-1] if state.get("messages") else None
    if last_message and hasattr(last_message, 'tool_calls') and last_message.tool_calls:
        for tool_call in last_message.tool_calls:
            print(f"工具执行：{tool_call['name']}")
            print(f"工具执行参数：{tool_call.get('args', {})}")
    return state


class MockAgent:
    def __init__(self, tools):
        self.tools = {t.name: t for t in tools}
    
    def invoke(self, input_data):
        state = input_data.copy()
        
        log_before_agent(state)
        log_before_model(state)
        model_call_hook(state)
        
        user_message = state["messages"][-1]
        content = user_message["content"]
        
        if "天气" in content:
            city = "广州" if "广州" in content else "未知城市"
            tool_call_message = AIMessage(
                content="",
                tool_calls=[{"id": "call_123", "name": "get_weather", "args": {"city": city}}]
            )
            state["messages"].append(tool_call_message)
            
            monitor_tool(state)
            
            tool_result = self.tools["get_weather"].invoke({"city": city})
            tool_message = ToolMessage(
                content=tool_result,
                tool_call_id="test_call_id"
            )
            state["messages"].append(tool_message)
        
        final_response = AIMessage(content=f"根据查询，{city}的天气是晴天")
        state["messages"].append(final_response)
        
        log_after_model(state)
        log_after_agent(state)
        
        return state


agent = MockAgent(tools=[get_weather])

res = agent.invoke({"messages": [{"role": "user", "content": "今天广州天气如何"}]})

print("\n=== 输出结果 ===")
for message in res["messages"]:
    if isinstance(message, (HumanMessage, AIMessage)):
        print(f"{message.type}: {message.content}")
    elif isinstance(message, ToolMessage):
        print(f"tool: {message.content}")
