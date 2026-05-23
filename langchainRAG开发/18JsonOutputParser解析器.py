from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

str_parser = StrOutputParser()
json_parser = JsonOutputParser()

model = ChatOpenAI(
    model="qwen3.6-plus",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    api_key="sk-18f59fad818846f3b74f24a08863731a",
    streaming=False,  # 禁用流式输出，因为我们需要先解析 JSON
)

first_prompt = PromptTemplate.from_template(
    "我姓{lastname}，刚生了{gender}娃，请帮我起名，并返回起名结果的json字符串，仅告知我名字无需说其他内容，要求的key是name，value就是起的名字。请严格遵守格式要求"
)

second_prompt = PromptTemplate.from_template("姓名{name}，请帮我解析含义")

chain = first_prompt | model | json_parser | second_prompt | model | str_parser

for chunk in chain.stream({"lastname": "周", "gender": "女"}):
    print(chunk, end="", flush=True)

