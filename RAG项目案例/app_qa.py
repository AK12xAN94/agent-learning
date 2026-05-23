import streamlit as st
import config_data as config
from rag import RagService

st.title("智能客服")
st.divider()

if "rag" not in st.session_state:
    st.session_state.rag = RagService()

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "你好,我是智能客服,我可以帮助您解决问题."}
    ]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

prompt = st.chat_input("请输入您的问题")

if prompt:
    st.chat_message("user").write(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        with st.spinner("思考中..."):
            try:
                for chunk in st.session_state.rag.chat_stream(prompt):
                    full_response += chunk
                    message_placeholder.markdown(full_response + "▌")
                message_placeholder.markdown(full_response)
            except Exception as e:
                error_msg = f"❌ 出错了: {str(e)}"
                message_placeholder.markdown(error_msg)
                full_response = error_msg

        st.session_state.messages.append(
            {"role": "assistant", "content": full_response}
        )
