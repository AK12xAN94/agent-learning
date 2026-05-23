from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

prompt = PromptTemplate.from_template("你是一位专业的{name}，接下来你要回答我的问题：{question}！")

prompt.format(name="宝可梦对战大师", question="最强的mega宝可梦是哪个")
model = ChatOpenAI(
    model="qwen3.6-plus",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    api_key="sk-18f59fad818846f3b74f24a08863731a",
    streaming=True
)
res = model.stream(prompt.format(name="宝可梦对战大师", question="最强的mega宝可梦是哪个"))
for chunk in res:
    print(chunk.content, end="", flush=True)