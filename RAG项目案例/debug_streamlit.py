"""
诊断脚本：检查 Streamlit 运行时的目录和配置问题
"""
import os
import sys

print("=" * 60)
print("📋 诊断：Streamlit 目录和配置问题")
print("=" * 60)

# 检查当前工作目录
print(f"\n1. 当前工作目录 (cwd):")
print(f"   {os.getcwd()}")

# 检查脚本所在目录
script_dir = os.path.dirname(os.path.abspath(__file__))
print(f"\n2. 脚本所在目录:")
print(f"   {script_dir}")

# 检查相对路径配置
print(f"\n3. config_data.py 中的配置:")
print(f"   md5_path = './md5.txt'")
print(f"   persist_directory = './chroma_db'")
print(f"   这些是相对路径，取决于运行时的工作目录!")

# 检查文件是否存在（从脚本目录）
print(f"\n4. 从脚本目录检查文件:")
md5_path_script = os.path.join(script_dir, "md5.txt")
chroma_path_script = os.path.join(script_dir, "chroma_db")
print(f"   md5.txt 存在: {os.path.exists(md5_path_script)}")
print(f"   chroma_db 存在: {os.path.exists(chroma_path_script)}")

# 检查从 cwd 检查文件
print(f"\n5. 从当前工作目录检查文件:")
md5_path_cwd = os.path.join(os.getcwd(), "md5.txt")
chroma_path_cwd = os.path.join(os.getcwd(), "chroma_db")
print(f"   md5.txt 存在: {os.path.exists(md5_path_cwd)}")
print(f"   chroma_db 存在: {os.path.exists(chroma_path_cwd)}")

# 对比两者的 md5.txt 内容
print(f"\n6. 对比 md5.txt 内容:")
if os.path.exists(md5_path_script) and os.path.exists(md5_path_cwd):
    if md5_path_script == md5_path_cwd:
        print("   两者是同一个文件")
    else:
        with open(md5_path_script, 'r') as f:
            content_script = f.read()
        with open(md5_path_cwd, 'r') as f:
            content_cwd = f.read()
        print(f"   脚本目录 md5.txt: {content_script[:50]}...")
        print(f"   cwd md5.txt: {content_cwd[:50]}...")
        print("   ⚠️ 两个不同的 md5.txt 文件!")
else:
    print(f"   脚本目录: {md5_path_script} - 存在: {os.path.exists(md5_path_script)}")
    print(f"   cwd: {md5_path_cwd} - 存在: {os.path.exists(md5_path_cwd)}")

# 检查向量库
print(f"\n7. 检查向量库中的数据:")
try:
    from langchain_chroma import Chroma
    from langchain_community.embeddings import DashScopeEmbeddings

    # 从脚本目录加载
    embeddings = DashScopeEmbeddings(
        model="text-embedding-v3",
        dashscope_api_key="sk-18f59fad818846f3b74f24a08863731a"
    )

    # 检查脚本目录的向量库
    vector_store_script = Chroma(
        collection_name="rag",
        embedding_function=embeddings,
        persist_directory=os.path.join(script_dir, "chroma_db"),
    )
    results_script = vector_store_script.get()
    print(f"   脚本目录向量库文档数: {len(results_script['documents'])}")

    # 检查 cwd 的向量库
    vector_store_cwd = Chroma(
        collection_name="rag",
        embedding_function=embeddings,
        persist_directory=os.path.join(os.getcwd(), "chroma_db"),
    )
    results_cwd = vector_store_cwd.get()
    print(f"   cwd 向量库文档数: {len(results_cwd['documents'])}")

    if results_script['documents'] != results_cwd['documents']:
        print("   ⚠️ 两个向量库内容不同!")

except Exception as e:
    print(f"   检查向量库失败: {e}")

print("\n" + "=" * 60)
print("💡 如果发现有两个不同的 md5.txt 或 chroma_db，")
print("   说明 Streamlit 运行时的 cwd 与脚本目录不一致，")
print("   导致数据存储到了不同位置!")
print("=" * 60)