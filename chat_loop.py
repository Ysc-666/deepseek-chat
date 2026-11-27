# 步骤 3：多轮对话（终端版）
# 目标：一轮轮连续对话，messages 列表保存历史，AI 能记住上文
# 运行方式：在本文件所在目录执行  python chat_loop.py
# 退出方式：输入 exit（或 quit、退出）后回车

import os
import requests

try:
    from config import API_KEY
except ImportError:
    API_KEY = os.environ["API_KEY"]

# 接口地址与请求头
URL = "https://api.deepseek.com/chat/completions"
headers = {
    "Authorization": "Bearer " + API_KEY,
    "Content-Type": "application/json",
}
MODEL = "deepseek-flash"

# 3) 消息历史列表：每一轮的 user（你）和 assistant（AI）消息都追加到这里
messages = []

print("开始对话，输入 exit 退出。\n")

# 4) 循环：一直对话，直到输入退出词
while True:
    # 4.1 读取用户输入，去掉首尾空格
    user_input = input("你：").strip()

    # 退出判断
    if user_input.lower() in ("exit", "quit", "退出"):
        print("再见！")
        break
    # 空输入不发请求，直接继续下一轮
    if not user_input:
        continue

    # 4.2 把这一轮的用户消息追加进历史
    messages.append({"role": "user", "content": user_input})

    # 4.3 把整个历史列表一起发给 API
    payload = {"model": MODEL, "messages": messages}
    resp = requests.post(
        URL,
        headers=headers,
        json=payload,
        timeout=30,
        proxies={"http": None, "https": None},  # 直连，绕过本地代理
    )

    # 4.4 请求失败：打印状态码和原始返回，并撤回刚加的用户消息，避免脏历史
    if resp.status_code != 200:
        print("请求失败，状态码：", resp.status_code)
        print(resp.text)
        messages.pop()
        continue

    # 4.5 成功：取出 AI 回答，追加进历史，再打印
    data = resp.json()
    answer = data["choices"][0]["message"]["content"]
    messages.append({"role": "assistant", "content": answer})

    print("AI：" + answer)
    print()
