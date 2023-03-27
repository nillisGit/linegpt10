from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import os
import openai


app = Flask(__name__)

line_bot_api = LineBotApi(os.getenv("token"))



@app.route('/')
def home():
    return 'H3small!'


if __name__ == "__main__":
    app.run()
