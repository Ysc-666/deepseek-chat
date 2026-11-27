import os
from flask import Flask,request
import requests

try:
    from config import API_KEY
except ImportError:
    API_KEY = os.environ["API_KEY"]

URL = "https://api.deepseek.com/chat/completions"

headers = {
    "Authorization" : "Bearer " + API_KEY,
    "Content-Type" : "application/json"
}


app = Flask(__name__)

# 页面样式：页面背景、居中卡片、标题、输入框、按钮、回答区
STYLE = """
<style>
  * { box-sizing: border-box; }
  body {
    margin: 0; min-height: 100vh;
    display: flex; align-items: center; justify-content: center;
    background: #f2f4f7;
    font-family: -apple-system, "Segoe UI", "Microsoft YaHei", sans-serif;
  }
  .card {
    background: #fff; width: 100%; max-width: 480px;
    border-radius: 12px; box-shadow: 0 4px 16px rgba(0,0,0,.1);
    padding: 28px;
  }
  h1 { font-size: 20px; text-align: center; margin: 0 0 20px; }
  input[name=question] {
    width: 100%; padding: 10px 12px;
    border: 1px solid #d0d5dd; border-radius: 8px; font-size: 15px;
  }
  button {
    margin-top: 14px; width: 100%; padding: 10px;
    background: #4a90d9; color: #fff; border: 0; border-radius: 8px;
    font-size: 15px; cursor: pointer;
  }
  button:hover { background: #3a7bc2; }
  .answer {
    margin-top: 18px; background: #f0f5fa;
    border-radius: 8px; padding: 14px; line-height: 1.6;
  }
  .error { margin-top: 18px; color: #c0392b; }
  a { display: block; margin-top: 14px; text-align: center; color: #4a90d9; text-decoration: none; }
</style>
"""

def page(body):
    """把卡片内容包成完整 HTML 页面"""
    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <title>DeepSeek 问答</title>
  {STYLE}
</head>
<body>
  <div class="card">
    {body}
  </div>
</body>
</html>"""


@app.route("/",methods=["GET","POST"])
def test_function():
    if request.method == "POST":
        question = request.form["question"]
        payload = {"model": "deepseek-flash", "messages": [{"role": "user", "content": question}]}
        resp = requests.post(URL, headers=headers, json=payload, timeout=30, proxies={"http": None, "https": None})
        if resp.status_code != 200:
            body = "<h1>DeepSeek 问答</h1>" \
                   "<div class='error'>Request failed, status code: " + str(resp.status_code) + "</div>" \
                   "<a href='/'>返回</a>"
            return page(body)
        data = resp.json()
        answer = data["choices"][0]["message"]["content"]
        body = "<h1>DeepSeek 问答</h1>" \
               "<div class='answer'>AI answers: " + answer + "</div>" \
               "<a href='/'>再问一次</a>"
        return page(body)

    form = "<h1>DeepSeek 问答</h1>" \
           "<form method='POST' action='/'>" \
           "<input name='question' type='text' placeholder='输入你的问题…'>" \
           "<button type='submit'>提问</button>" \
           "</form>"
    return page(form)


if __name__ == "__main__":
    app.run()
