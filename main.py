from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    AudioMessage, ImageMessage, MessageEvent, TextMessage, TextSendMessage,
    TemplateSendMessage, ButtonsTemplate, MessageAction
)
import os
import json
import random
import requests
import re

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


#メッセージ判定イベントハンドラ
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    text = event.message.text
    if text == "こんにちは":
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="こんにちは"))
    elif re.match('.*(お腹|おなか|).*(すいた|空いた).*', text):
        url='https://api.gnavi.co.jp/RestSearchAPI/v3/?keyid=93af8ad3c31d026bbd4801aaa738b64d&pref=PREF40&area=AREA140&areacode_m=AREAM5114'
        html=requests.get(url)
        data=json.loads(html.text)

        rest = data['rest']
        choi = random.choice(rest)
        res = "店名："+choi['name']+"\n"+choi['url']
        image = choi['image_url']['shop_image1']
        #こっから
        buttons_template_message = TemplateSendMessage(
            alt_text='Buttons template',
            template=ButtonsTemplate(
            thumbnail_image_url='https://example.com/image.jpg',
            title='Menu',
            text='Please select',
            actions=[
                MessageAction(
                    label='message',
                    text='message text'
                )
            ]
            )
        )

        line_bot_api.reply_message(event.reply_token, messages=buttons_template_message)
        #ここまで
    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="「お腹すいた」と言ってみよう！"+"\n"+"箱崎のお店をランダムに紹介するよ！！"))

#画像入力判定イベントハンドラ
@handler.add(MessageEvent, message=ImageMessage)
def handle_image(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text="画像入力は対応していません"))

#音声入力判定イベントハンドラ
@handler.add(MessageEvent, message=AudioMessage)
def handle_audio(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text="音声入力は対応していません"))

if __name__ == "__main__":
#    app.run()
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
