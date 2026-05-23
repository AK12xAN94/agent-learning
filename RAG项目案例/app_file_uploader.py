import streamlit as st
from knowledge_base import KnowledgeBaseService
import time

# 标题
st.title("知识库更新服务")

# file uploader
file_uploader = st.file_uploader("上传文件", type=["txt", "pdf", "docx"])

if 'service' not in st.session_state:
    st.session_state.service = KnowledgeBaseService()
    st.session_state.upload_history = []

if file_uploader is not None:
    file_name = file_uploader.name
    file_type = file_uploader.type
    file_size = file_uploader.size / 1024
    st.subheader(f"📄 文件信息 - {file_name}")
    col1, col2 = st.columns(2)
    with col1:
        st.text(f"类型: {file_type}")
    with col2:
        st.text(f"大小: {file_size:.2f} KB")

    # 读取文件内容
    try:
        text = file_uploader.getvalue().decode("utf-8")
        st.text_area("文件预览", value=text, height=150, disabled=True)
    except Exception as e:
        st.error(f"❌ 读取文件失败: {str(e)}")
        text = None

    if text:
        if st.button("🚀 上传到知识库", type="primary"):
            with st.spinner("正在上传到知识库..."):
                try:
                    result = st.session_state.service.upload_by_str(text, file_name)

                    # 根据结果显示不同的样式
                    if "[跳过]" in result:
                        st.warning("⚠️ " + result)
                        st.info("💡 提示：该文件内容之前已经上传过。如需重新上传，请先删除 md5.txt 文件中的对应记录。")
                    elif "[成功]" in result:
                        st.success("✅ " + result)
                        # 添加到历史记录
                        st.session_state.upload_history.append({
                            "filename": file_name,
                            "result": result,
                            "size": f"{file_size:.2f} KB"
                        })
                    else:
                        st.info(result)

                except Exception as e:
                    st.error(f"❌ 上传失败: {str(e)}")
                    st.exception(e)

# 显示上传历史
if st.session_state.upload_history:
    st.divider()
    st.subheader("📜 上传历史")
    for item in reversed(st.session_state.upload_history[-5:]):
        with st.expander(f"✅ {item['filename']} - {item['size']}"):
            st.text(item['result'])