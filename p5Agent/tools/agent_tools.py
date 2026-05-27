from langchain_core.messages import tool
from langchain_core.tools import tool
import os

import random
from AI大模型与RAG.p5Agent.utils.config_handler import agent_config
from AI大模型与RAG.p5Agent.utils.path_tool import get_abs_path
from p5Agent.rag.rag_service import RagSummarizeService

external_data_path = {}
rag = RagSummarizeService()

user_ids = ['1001', '1002', '1003', '1004', '1005', '1006', '1007', '1008', '1009', '1010']
month_arr = ['2025-01', '2025-02', '2025-03', '2025-04', '2025-05', '2025-06', '2025-07', '9月', '10月', '11月', '12月']
external_data = {}

@tool(description="从向量存储中检索参考资料")
def rag_summarize(query: str) -> str:
    return rag.rag_summarize(query)

@tool(description="获取指定城市的天气，以消息字符串的形式返回")
def get_weather(city: str) -> str:
    return f"{city}的天气为晴天，气温26摄氏度，空气湿度50%，南风一级，AQI21，最近6小时降雨概率极低"
   
@tool(description="获取指定用户的当前位置，以消息字符串的形式返回")
def get_user_location() -> str:
    return random.choice(['深圳', '北京', '广州', '上海'])


@tool(description="获取指定用户的ID，以纯字符串的形式返回")
def get_user_id() -> str:
    return random.choice(user_ids)

@tool(description="获取当前月份的天数，以纯字符串的形式返回")
def get_current_month() -> str:
    return random.choice(month_arr)

@tool(description="从外部数据源获取用户数据，以纯字符串形式返回，如果未检索到则返回字符串")
def fetch_external_data(user_id: str, month: str) -> str:
    return f"用户{user_id}在{month}的外部数据"

def generate_external_data():
    if not external_data:
        external_data_path = get_abs_path(agent_config["external_data_path"])

        if not os.path.exists(external_data_path):
            print(f"外部数据文件 {external_data_path} 不存在")
            raise FileNotFoundError(f"外部数据文件 {external_data_path} 不存在")
            
        with open(external_data_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()[1:]
            for line in lines:
                line = line.strip()
                if line:
                    arr: list[str] = line.split(',')
                    user_id: str = arr[0].replace('"', '')
                    feature: str = arr[1].replace('"', '')
                    efficiency: str = arr[2].replace('"', '')
                    consumable: str = arr[3].replace('"', '')
                    comparision: str = arr[4].replace('"', '')
                    time: str = arr[5].replace('"', '')

                    if user_id not in external_data:
                        external_data[user_id] = {}
                    external_data[user_id][time] = {
                        "feature": feature,
                        "efficiency": efficiency,
                        "consumable": consumable,
                        "comparision": comparision,
                    }

@tool(description="从外部数据源获取用户数据，以纯字符串形式返回，如果未检索到则返回字符串")
def fetch_external_data(user_id: str, month: str) -> str:

    generate_external_data()

    try:
        if user_id not in external_data:
            return f"用户{user_id}在{month}没有外部数据"
        if month not in external_data[user_id]:
            return f"用户{user_id}在{month}没有外部数据"
        return f"用户{user_id}在{month}的外部数据为：{external_data[user_id][month]}"
    except KeyError as e:
        return f"用户{user_id}在{month}没有外部数据"
