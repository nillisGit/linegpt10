import os
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import openai
#from dotenv import load_dotenv

#load_dotenv()
app = Flask(__name__)

# Line bot 設定

CHANNEL_ACCESS_TOKEN = os.getenv('CHANNEL_ACCESS_TOKEN')
CHANNEL_SECRET = os.getenv('CHANNEL_SECRET')

line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)

# OpenAI 設定
OpenAIkey = os.getenv('OpenAIkey')

openai.api_key = OpenAIkey
model_engine = "davinci"

def generate_response(user_message):
    prompt = (f"The following is a conversation with a user about {user_message}. The user says:") # 設定 GPT-3 問題
    response = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )
    message = response.choices[0].text.strip() # 獲得 GPT-3 回答
    return message


@app.route('/')
def home():
    return "Home base"


# 設定 Line bot 的 Webhook
@app.route("/Webhook", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return "OK"

# 設定 Line bot 回應
@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    user_message = event.message.text
    reply_message = generate_response(user_message) # 使用 GPT-3 API 產生回應
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_message))

# 啟動 Flask
if __name__ == "__main__":
    #app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
    app.run()