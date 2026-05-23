"""
诊断脚本：测试向量存储流程
"""

import os
import sys
import hashlib

# 添加当前目录到 path
current_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(current_dir)


def test_upload_flow():
    """测试上传流程"""
    print("=" * 60)
    print("📋 诊断测试：文件上传和向量存储流程")
    print("=" * 60)

    # 1. 模拟读取文件
    file_path = os.path.join(current_dir, "data", "尺码推荐.txt")
    print(f"\n✅ 步骤1: 检查文件存在性")
    print(f"   文件路径: {file_path}")
    print(f"   文件存在: {os.path.exists(file_path)}")

    if not os.path.exists(file_path):
        print("   ❌ 文件不存在!")
        return

    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()

    print(f"   ✅ 成功读取文件，字符数: {len(text)}")
    print(f"   前100字符: {text[:100]}...")

    # 2. 检查 MD5
    md5_hex = hashlib.md5(text.encode("utf-8")).hexdigest()
    print(f"\n✅ 步骤2: 计算文件 MD5")
    print(f"   MD5 = {md5_hex}")

    # 3. 检查 md5.txt
    md5_file_path = os.path.join(current_dir, "md5.txt")
    print(f"\n✅ 步骤3: 检查 md5.txt")
    print(f"   文件路径: {md5_file_path}")
    print(f"   文件存在: {os.path.exists(md5_file_path)}")

    if os.path.exists(md5_file_path):
        with open(md5_file_path, "r", encoding="utf-8") as f:
            existing_md5s = f.readlines()
        print(f"   已有名: {len(existing_md5s)} 条记录")
        for md5 in existing_md5s:
            md5_stripped = md5.strip()
            match = " ✓ (与当前文件相同，会被跳过!)" if md5_stripped == md5_hex else ""
            print(f"   - {md5_stripped}{match}")
    else:
        print("   ⚠️ md5.txt 不存在，将创建新文件")

    # 4. 创建服务并上传
    print(f"\n✅ 步骤4: 调用 upload_by_str")

    from knowledge_base import KnowledgeBaseService

    service = KnowledgeBaseService()

    result = service.upload_by_str(text, os.path.basename(file_path))
    print(f"   上传结果: {result}")

    if "[跳过]" in result:
        print("\n" + "=" * 60)
        print("⚠️ 问题发现：文件被跳过了!")
        print("=" * 60)
        print("原因: 该文件之前已经上传过，MD5 记录存在于 md5.txt 中。")
        print("解决方案: 需要从 md5.txt 中删除对应的 MD5 记录，或者")
        print("         删除 md5.txt 文件后重新上传。")
        print("=" * 60)
    elif "[成功]" in result:
        print("\n" + "=" * 60)
        print("✅ 文件已成功添加到向量库!")
        print("=" * 60)

    # 5. 检查向量库
    print(f"\n✅ 步骤5: 验证向量库")
    from langchain_chroma import Chroma
    from langchain_community.embeddings import DashScopeEmbeddings

    embeddings = DashScopeEmbeddings(
        model="text-embedding-v3",
        dashscope_api_key="sk-18f59fad818846f3b74f24a08863731a",
    )

    vector_store = Chroma(
        collection_name="rag",
        embedding_function=embeddings,
        persist_directory="./chroma_db",
    )

    results = vector_store.get()
    print(f"   向量库中共有 {len(results['documents'])} 条文档")

    for i, doc in enumerate(results["documents"]):
        print(f"\n   文档 {i + 1}:")
        print(f"   内容: {doc[:100]}..." if len(doc) > 100 else f"   内容: {doc}")
        print(f"   源: {results['metadatas'][i].get('source', 'N/A')}")


if __name__ == "__main__":
    test_upload_flow()
