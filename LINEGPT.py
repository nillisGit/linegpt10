import os
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import openai

app = Flask(__name__)

# Line bot 設定
CHANNEL_ACCESS_TOKEN = 'kD/dPujEGje9QnQAVcqTFID55LvykQLjkZZ20Hu9BAh4qqZEH9zxUsoKbR6J2+Twq844syLSak60UUYJF3blJn+98fULP4tQrXCttjR/4ojK3W7HepKxeB+3wbSO+PKZTPdTP44P5yR8pW/eslqzWgdB04t89/1O/w1cDnyilFU='
CHANNEL_SECRET = 'dcf6386a1de1d3109c596e81eb3c3055'

line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)

# OpenAI 設定
openai.api_key = "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"
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

# 設定 Line bot 的 Webhook
@app.route("/callback", methods=["POST"])
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
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
