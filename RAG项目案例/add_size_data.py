"""
手动添加尺码推荐到向量库
"""
from knowledge_base import KnowledgeBaseService
import os

# 读取尺码推荐文件
file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "颜色推荐.txt")

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

print(f"文件内容 ({len(content)} 字符):")
print(content)
print("\n" + "=" * 50 + "\n")

# 创建知识库服务
service = KnowledgeBaseService()

# 添加到向量库
result = service.upload_by_str(content, "颜色推荐.txt")
print(f"添加结果: {result}")