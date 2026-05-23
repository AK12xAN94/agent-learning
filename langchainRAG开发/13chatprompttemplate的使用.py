from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_openai import ChatOpenAI
# 创建一个更简洁的方式来处理消息历史
chat_prompt_template = ChatPromptTemplate.from_messages([
    ("system", "你是一个专业的{name}，接下来你要回答我的问题！"),
    # 动态消息历史将在 invoke 时传入
])

history_data = [
    HumanMessage(content="你来写一首唐诗"),
    AIMessage(content="床前明月光，疑是地上霜。举头望明月，低头思故乡。"),
    HumanMessage(content="好诗好诗，再来一首"),
    AIMessage(content="锄禾日当午，汗滴禾下土。谁知盘中餐，粒粒皆辛苦。"),
]

# 构建完整的消息列表
def build_messages(name, history):
    messages = []
    messages.append(SystemMessage(content=f"你是一个专业的{name}，接下来你要回答我的问题！"))
    messages.extend(history)
    messages.append(HumanMessage(content="请继续创作一首唐诗"))
    return messages

# 生成完整的消息列表
messages = build_messages("诗人", history_data)

# 打印消息内容
for msg in messages:
    print(f"{msg.type}: {msg.content}")
    print("-" * 40)

model = ChatOpenAI(
    model="qwen3.6-plus",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    api_key="sk-18f59fad818846f3b74f24a08863731a",
    streaming=True
)

res = model.stream(messages)
for chunk in res:
    print(chunk.content, end="", flush=True)