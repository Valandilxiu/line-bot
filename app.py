
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

line_bot_api = LineBotApi('14hQbKfxoIR1Nd6o0/mrj+gtQAp5KGkTg7vDJxyxNbkZ1NphUDQ2N1kvZ8iKEpQRWeZEXpL92ND6vW7khyNcUlJglK/rvdvGlNYKeSQY5jcaz6vNxu1sEa96UI4uV2kLL/Q8Y3SqVblEk53gcj7rwAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('747402ad64d3de425f1abcc493c59f4b')


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