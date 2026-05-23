"""
JSONLoader总结：
1. JSONLoader依赖jq库，通过pip install jq安装
2. JSONLoader使用jq的解析语法，常见如：
   - .表示根、[]表示数组
   - .name表示从根取name的值
   - .hobby[1]表示取hobby对应数组的第二个元素
   - .[]表示将数组内的每个字典（JSON对象）都取到
   - .[].name表示取数组内每个字典（JSON对象）的name对应的值
3. JSONLoader初始化有4个主要参数：
   - file_path: 文件路径，必填
   - jq_schema: jq解析语法，必填
   - text_content: 抽取到的是否是字符串，默认True，非必填
   - json_lines: 是否是JsonLines文件，默认False，非必填
4. JsonLines文件：每一行都是一个独立的字典（Json对象）
"""

from langchain_community.document_loaders import JSONLoader
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
json_path = os.path.join(current_dir, "data", "stu.json")

loader = JSONLoader(
    file_path=json_path,
    jq_schema=".other .addr",
    # text_content=True 会将json文件内容作为字符串加载，而不是解析为json对象
    # jsonlines=True 告诉Loader文件是jsonlines格式，每个json对象占一行
)
docs = loader.load()
for doc in docs:
    print(type(doc), doc.page_content)
