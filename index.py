import os
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

app = Flask(__name__)

line_bot_api = LineBotApi(os.getenv('CHANNEL_ACCESS_TOKEN'))
hh = WebhookHandler(os.getenv("CHANNEL_SECRET"))
openai.api_key = os.getenv('OpenKey')

@app.route('/')
def home():
    return 'H3small!'



@app.route('/webhook', methods=['POST'])
def webhook():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        hh.handle(body, signature)        
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@hh.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    #user_message = event.message.text
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text='Reply:'+ 'go'))


if __name__ == '__main__':
    app.run()
