from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnableLambda

str_parser = StrOutputParser()
my_func = RunnableLambda(lambda ai_msg: {"name": ai_msg})

model = ChatOpenAI(
    model="qwen3.6-plus",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    api_key="sk-18f59fad818846f3b74f24a08863731a",
    streaming=True
)

first_prompt = PromptTemplate.from_template("我姓{lastname}，刚生了{gender}娃，请帮我起名，仅告知我名字无需说其他内容")

second_prompt = PromptTemplate.from_template("姓名{name}，请帮我解析含义")

chain = first_prompt | model | str_parser | my_func | second_prompt | model | str_parser

res = chain.stream({"lastname": "周", "gender": "女"})
for chunk in res:
    print(chunk, end="", flush=True)
