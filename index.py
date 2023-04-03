import os
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import openai

app = Flask(__name__)



line_bot_api = LineBotApi(os.getenv('CHANNEL_ACCESS_TOKEN'))
hh = WebhookHandler(os.getenv("CHANNEL_SECRET"))
openai.api_key = os.getenv('OpenAIkey')

@app.route('/')
def home():
    return 'H3small!'

@app.route("/webhook", methods=["POST"])
def webhook():
    signature = request.headers["X-Line-Signature"]
    body = request.get_data(as_text=True)
    try:
        hh.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'
    
@hh.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    user_message = event.message.text
    ######
    print(user_message)
    prompt = (f"Message==> {user_message}. GPT replys:") 
    response = openai.Completion.create(
        engine="davinci",
        prompt=prompt,
        max_tokens=200,
        n=1,
        stop=None,
        temperature=0.5,
    )
    gptreply = response.choices[0].text.strip()     
    #line_bot_api.reply_message(event.reply_token, TextSendMessage(text=gptreply))
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=user_message))  

if __name__ == "__main__":
    app.run()
