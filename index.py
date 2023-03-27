from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import os
import openai


app = Flask(__name__)
line_bot_api = LineBotApi(os.getenv("token"))
handler = WebhookHandler(os.getenv("cs"))
openai.api_key = os.getenv("aikey")
model_engine = "davinci"




@app.route('/')
def home():
    return 'H3small!'


if __name__ == "__main__":
    app.run()
