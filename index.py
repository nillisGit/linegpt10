import os
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import openai
#from dotenv import load_dotenv

#load_dotenv()
app = Flask(__name__)


mm= os.getenv('CHANNEL_ACCESS_TOKEN')
line_bot_api = LineBotApi('Bearer ' + mm)
handler = WebhookHandler(os.getenv("CHANNEL_SECRET"))
#openai.api_key = os.getenv('OpenAIkey')
model_engine = "davinci"

@app.route('/')
def home():
    return "1531" #os.getenv("CHANNEL_SECRET")

# 啟動 Flask
if __name__ == "__main__":
    #app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
    app.run()
