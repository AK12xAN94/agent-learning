from openai import OpenAI
client = OpenAI(
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

response = client.chat.completions.create(
    model="qwen3.6-plus",
    messages=[
        {"role": "system", "content": "你是一个专业的宝可梦对战大师，话很多。"},
        {"role": "assistant", "content": "好的，我是一个专业的宝可梦对战大师，我可以回答你关于宝可梦对战的问题。"},
        {"role": "user", "content": "最强的mega宝可梦是哪个"},
        ],
    stream=True
)
for chunk in response:
    if chunk.choices:
        delta = chunk.choices[0].delta
        if hasattr(delta, "content") and delta.content:
            print(delta.content, end=" ", flush=True)
