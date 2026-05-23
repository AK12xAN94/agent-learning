import os, json
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import BaseMessage, messages_to_dict, messages_from_dict
from typing import Sequence

def get_history(session_id: str):
    """
    获取会话历史记录
    """
    return FileChatMessageHistory(session_id, os.path.join(os.path.dirname(__file__), "history"))

class FileChatMessageHistory(BaseChatMessageHistory):
    def __init__(self, session_id: str, storage_path: str):
        self.session_id = session_id
        self.storage_path = storage_path
        self.file_path = os.path.join(self.storage_path, f"{self.session_id}.json")
        
        os.makedirs(self.storage_path, exist_ok=True)

    def add_messages(self, messages: Sequence[BaseMessage]) -> None:
        all_messages = list(self.messages) + list(messages)

        new_messages = messages_to_dict(all_messages)
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(new_messages, f, ensure_ascii=False, indent=2)

    @property
    def messages(self) -> list[BaseMessage]:
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                messages_data = json.load(f)
                return messages_from_dict(messages_data)
        except FileNotFoundError:
            return []

    def clear(self) -> None:
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump([], f, ensure_ascii=False, indent=2)
