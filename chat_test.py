# 第一个 DeepSeek 调用脚本
# 目标：终端向 AI 提一个问题，打印出 AI 的一次回答
# 运行方式：在本文件所在目录执行  python chat_test.py

import os
import requests

try:
    from config import API_KEY
except ImportError:
    API_KEY = os.environ["API_KEY"]

# 接口地址（DeepSeek 兼容 OpenAI 格式的聊天接口）
URL = "https://api.deepseek.com/chat/completions"

# 3) 请求头：Authorization 用来证明身份，Content-Type 表示发的是 JSON
headers = {
    "Authorization": "Bearer " + API_KEY,
    "Content-Type": "application/json",
}

# 4) 请求内容：模型名称 + 消息列表（role 角色，content 内容）
#    起步用 deepseek-flash（快、便宜）；更强的可选 deepseek-v4-pro
payload = {
    "model": "deepseek-flash",
    "messages": [
        {"role": "user", "content": "你好，1+1是多少"}
    ],
}

# 5) 发出 POST 请求，等待服务器返回（timeout 最多等 30 秒）
#    proxies 置空 = 直连，绕过本机失效的 Clash 系统代理（DeepSeek 国内可直连）
resp = requests.post(
    URL,
    headers=headers,
    json=payload,
    timeout=30,
    proxies={"http": None, "https": None},
)

# 6) 判断结果：不成功就打印状态码和原始返回，方便排查；成功就取出回答
if resp.status_code != 200:
    print("请求失败，状态码：", resp.status_code)
    print(resp.text)
else:
    data = resp.json()
    answer = data["choices"][0]["message"]["content"]
    print("AI 回答：")
    print(answer)
