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

app = Flask(__name__)

line_bot_api = LineBotApi('m4k0P5Dd4d+DQlnlEWGNArhr5ZJLGaFPWCiO8YqLbUse4c9cBjQ5qYoP/NhXcrmZl2gq+MkGhUmsVCmA2cqx621eSTu+C8Cb4nXwcGYodU0j4gpzApGn89hFkb/iNNtVKJkjky/Q3HzzdT+sCzQSOAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('fdfba11b5865be64810ff2ac5824c49a')


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
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()