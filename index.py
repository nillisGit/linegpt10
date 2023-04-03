import os
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

app = Flask(__name__)

line_bot_api = LineBotApi(os.getenv('CHANNEL_ACCESS_TOKEN'))
hhan = WebhookHandler(os.getenv('CHANNEL_SECRET'))

@app.route('/')
def home():
    return 'H3small!'



@app.route('/webhook', methods=['POST'])
def webhook():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        hhan.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@hhan.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text='test reply'))

if __name__ == '__main__':
    app.run()
