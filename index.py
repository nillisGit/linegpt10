from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import os
import openai


app = Flask(__name__)

CHANNEL_SECRET = os.getenv('LINE_CHANNEL_SECRET')
handler = WebhookHandler(CHANNEL_SECRET)
print(CHANNEL_SECRET)


@app.route('/')
def home():
    return CHANNEL_SECRET


if __name__ == "__main__":
    app.run()
