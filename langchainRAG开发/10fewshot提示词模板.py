from langchain_core.prompts import PromptTemplate, FewShotPromptTemplate
from langchain_openai import ChatOpenAI

# 示例模板
example_template = PromptTemplate.from_template("单词：{word}，反义词：{antonym}")

# 示例数据
examples_data = [
    {"word": "好", "antonym": "坏"},
    {"word": "是", "antonym": "否"},
    {"word": "上", "antonym": "下"},
]

# 创建 FewShot 提示词模板
few_shot_prompt_template = FewShotPromptTemplate(
    example_prompt=example_template,  # 示例模板
    examples=examples_data,           # 示例数据
    prefix="请根据以下示例，填写缺失的反义词：",
    suffix="单词：{word}，反义词：",
    input_variables=["word"],
)

# 生成提示词
prompt = few_shot_prompt_template.invoke({"word": "美"}).to_string()
print(prompt)

model = ChatOpenAI(
    model="qwen3.6-plus",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    api_key="sk-18f59fad818846f3b74f24a08863731a",
    streaming=True
)

res = model.stream(prompt)
for chunk in res:
    print(chunk.content, end="", flush=True)