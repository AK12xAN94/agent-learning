from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

model = ChatOpenAI(
    model="qwen3.6-plus",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    api_key="sk-18f59fad818846f3b74f24a08863731a",
    streaming=True
)

prompt = PromptTemplate.from_template("我姓{lastname}，刚生了{gender}娃，请帮我起名，仅告知我名字无需说其他内容")
parser = StrOutputParser()
chain = prompt | model | parser

res = chain.invoke({"lastname": "周", "gender": "女"})
print(res)
