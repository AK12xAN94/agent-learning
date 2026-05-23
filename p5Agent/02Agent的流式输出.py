from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool


@tool(description="查询股票价格")
def get_price(name: str) -> str:
    return f"股票{name}的价格是100元"


@tool(description="查询股票信息")
def get_info(name: str) -> str:
    return f"股票{name}，是一家A股上市公司，专注于IT职业教育"


agent = create_agent(
    model=ChatOpenAI(
        model="qwen3.6-plus",
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    ),
    tools=[get_price, get_info],
    system_prompt="你是一个智能聊天助手.",
)

res = agent.stream(
    {"messages": [{"role": "user", "content": "传智教育的股价多少，并介绍一下"}]},
    stream_mode="values"

)
for chunk in res:
    last_message = chunk["messages"][-1]
    if last_message.content:
        print(last_message.content, end="", flush=True)

    try:
        if last_message.tool_calls:
            print(f"工具调用：{ [tc['name'] for tc in last_message.tool_calls]}")

    except AttributeError as e:
        pass
