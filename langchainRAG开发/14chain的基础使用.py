from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_openai import ChatOpenAI

# 定义消息历史
history_data = [
    HumanMessage(content="你来写一首唐诗"),
    AIMessage(content="床前明月光，疑是地上霜。举头望明月，低头思故乡。"),
    HumanMessage(content="好诗好诗，再来一首"),
    AIMessage(content="锄禾日当午，汗滴禾下土。谁知盘中餐，粒粒皆辛苦。"),
]

# 构建完整的消息列表
def build_messages(name, history, user_input):
    messages = []
    messages.append(SystemMessage(content=f"你是一个专业的{name}，接下来你要回答我的问题！"))
    messages.extend(history)
    messages.append(HumanMessage(content=user_input))
    return messages

# 生成完整的消息列表
messages = build_messages("诗人", history_data, "请继续创作一首唐诗")

# 打印消息内容
print("消息历史：")
for msg in messages:
    print(f"{msg.type}: {msg.content}")
    print("-" * 40)

# 创建模型
model = ChatOpenAI(
    model="qwen3.6-plus",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    api_key="sk-18f59fad818846f3b74f24a08863731a",
    streaming=True
)

# 直接调用模型（不使用 chain，因为我们已经有完整的消息列表）
print("\nAI 回复：")
for chunk in model.stream(messages):
    print(chunk.content, end="", flush=True)