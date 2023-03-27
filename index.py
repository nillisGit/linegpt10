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
hh = WebhookHandler(os.getenv("CHANNEL_SECRET"))
openai.api_key = os.getenv('OpenAIkey')
model_engine = "davinci"

def generate_response(user_message):
    prompt = (f"The following is a conversation with a user about {user_message}. The user says:") 
    response = openai.Completion.create(
        engine="davinci",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )
    message = response.choices[0].text.strip() 
    return message

@app.route('/')
def home():
    return 'H3small!'


@app.route("/webhook", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    body = request.get_data(as_text=True)
    try:
        hh.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return "OK"

@hh.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    user_message = event.message.text
    reply_message = generate_response(user_message)
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_message))

if __name__ == "__main__":
    app.run()
