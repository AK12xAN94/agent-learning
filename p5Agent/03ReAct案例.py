from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool


@tool(description="获取体重，返回值是整数，单位是千克")
def get_weight() -> int:
    return 90


@tool(description="获取身高，返回值是整数，单位是厘米")
def get_height() -> int:
    return 180


agent = create_agent(
    model=ChatOpenAI(
        model="qwen3.6-plus",
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    ),
    tools=[get_weight, get_height],
    system_prompt="你是严格遵守ReAct框架的智能体，必须按【思考->行动->观察->思考】的流程解决问题。且**每轮仅能思考并调用一个工具**，不能同时调用多个工具。并告诉我你的思考过程，工具的调用原因，按思考、行动、观察三个结构告知我。",
)

res = agent.stream(
    {"messages": [{"role": "user", "content": "计算我的BMI"}]},
    stream_mode="values",
)
for chunk in res:
    last_message = chunk["messages"][-1]
    if last_message.content:
        print(last_message.content, end="", flush=True)

    try:
        if last_message.tool_calls:
            print(f"工具调用：{[tc['name'] for tc in last_message.tool_calls]}")

    except AttributeError as e:
        pass
