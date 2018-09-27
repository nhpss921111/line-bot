# 網頁開發程式
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, StickerSendMessage
)

app = Flask(__name__)

line_bot_api = LineBotApi('6bWHiEdep6VDd7Rv4sdTfgGlx1P037s1k7AQM/E5ttlEFyfc2AbwPXdNfSWXU8q9Hpzg7yYV8Xa8jhgn3gRnOfNBZah4I+w0vdcpeSnRwgPt0nNWbIEVrSTiI/+qqDqDskMDcGS8faOv6agiDZpt9QdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('75454b50ab951ee7163c091c48ff5a47')


@app.route("/callback", methods=['POST'])
# 接收line傳來的訊息
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
    msg = event.message.text
    r = '你說甚麼我看不懂XD'

    if msg in '給我貼圖':
        sticker_message = StickerSendMessage(
            package_id='1',
            sticker_id='410'
        )
        line_bot_api.reply_message(
        event.reply_token,
        sticker_message)

    if msg in ['hi', 'Hi', '嗨','你好']:
        r = '嗨，要不要來買便當？'
    elif msg == '我要點餐':
        r = '菜單請看大頭貼，謝謝'
    elif '飯' in msg:
        r = '內用還是外帶？'
    elif msg == '可以外送嗎？':
        r = '不好意思，現在人手不足無法外送！'

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=r))


if __name__ == "__main__":
    app.run()