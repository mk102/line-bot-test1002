from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)
import os
import json
import random
import requests

app = Flask(__name__)

#環境変数取得
YOUR_CHANNEL_ACCESS_TOKEN = os.environ["YOUR_CHANNEL_ACCESS_TOKEN"]
YOUR_CHANNEL_SECRET = os.environ["YOUR_CHANNEL_SECRET"]

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    text = event.message.text
    if text == "こんにちは":
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="こんにちは"))
    else:
        url='https://api.gnavi.co.jp/RestSearchAPI/v3/?keyid=93af8ad3c31d026bbd4801aaa738b64d&pref=PREF40&area=AREA140&areacode_m=AREAM5114'
        html=requests.get(url)
        data=json.loads(html.text)

        rest = data['rest']
        choi = random.choice(rest)
        
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=choi['name']))


if __name__ == "__main__":
#    app.run()
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
