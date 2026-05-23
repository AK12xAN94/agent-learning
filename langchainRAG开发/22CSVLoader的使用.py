"""
LangChain文档加载器总结：
1. LangChain内置了许多种类的文档加载器
2. 文档加载器均继承于BaseLoader类
3. 返回Document类型的对象
4. load方法一次性批量加载（返回list内含Document对象），如内容过多可能list太大，出现内存溢出问题
5. lazy_load方法会得到生成器对象，可用for循环依次获取单个Document对象，适用于大文档避免内存存不下
6. CSVLoader用于加载CSV文件，加载成功得到的即Document对象
"""

from langchain_community.document_loaders import CSVLoader
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(current_dir, "data", "stu.csv")

# 批量加载CSV文件 .load()
loader = CSVLoader(
    file_path=csv_path,
    csv_args={
        "delimiter": "|",  # 自定义分隔符
    },
    encoding="utf-8",
)
docs = loader.load()
for doc in docs:
    print(type(doc), doc.page_content)

# 懒加载 .lazy_load()
for doc in loader.lazy_load():
    print(doc.page_content)
