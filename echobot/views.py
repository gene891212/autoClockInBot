# coding=utf-8
from django.shortcuts import render

# Create your views here.
import requests
import os
from echobot.myFunction import *
from echobot.models import UserInformation

from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http.request import HttpRequest
from django.http.response import HttpResponse, HttpResponseBadRequest
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *

from selenium.common.exceptions import NoSuchElementException

line_bot_api = LineBotApi(os.environ['CHANNEL_ACCESS_TOKEN'])
handler = WebhookHandler(os.environ['CHANNEL_SECRET'])

# rich menu
rich_menu_id = line_bot_api.create_rich_menu(rich_menu=init_rich_menu())
with open('richmenu.png', 'rb') as f:
    line_bot_api.set_rich_menu_image(rich_menu_id, 'image/png', f)
line_bot_api.set_default_rich_menu(rich_menu_id)

# db
all_user_id = list(map(lambda entry: entry.user_id, UserInformation.objects.all()))


@csrf_exempt
@require_POST
def webhook(request: HttpRequest):
    signature = request.headers["X-Line-Signature"]
    body = request.body.decode()

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        messages = (
            "Invalid signature. Please check your channel access token/channel secret."
        )
        logger.error(messages)
        return HttpResponseBadRequest(messages)
    return HttpResponse("OK")

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    print(event)
    if event.source.user_id != "Udeadbeefdeadbeefdeadbeefdeadbeef":
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=event.message.text)
        )

@handler.add(PostbackEvent)
def handle_message(event):
    # print(event)
    # print(event.source.user_id)
    if event.postback.data == 'check':
        push_sticker_message(event, 'Linebot is Online.', '11537', '52002746')
    elif event.postback.data == 'clockIn':
        # line_bot_api.push_message(
        #     event.source.user_id,
        #     tempConfirmTemplate()
        # )
        reply_message(event, 'ClockIn Now...')
        user_detail = UserInformation.objects.get(user_id=event.source.user_id)
        try:
            echo = ClockIn(event).clockIn(user_detail.email_account, user_detail.email_password)
        except NoSuchElementException as e:
            push_message(event, e)
        else:
            push_sticker_message(event, echo, '11537', '52002734')
        # line_bot_api.broadcast(TextSendMessage(text='說個話吧'))
    else:
        pass

@handler.add(FollowEvent)
def handle_message(event):
    print(event)
    if event.source.user_id not in all_user_id:
        profile = line_bot_api.get_profile(event.source.user_id)
        UserInformation(user_id=profile.user_id, user_name=profile.display_name).save()
        text = f'Hi Hi {profile.display_name}, I\'m writing your information into database. You can not reject.'
        push_sticker_message(event, text, '11537', '52002753')


# {"mode": "active", "postback": {"data": "clockIn"}, "replyToken": "02c2fc5a1c9844789ef9c4226d29153d", 
#  "source": {"type": "user", "userId": "Ub1eff16cb01f4343694423cba8c74e52"}, 
#  "timestamp": 1603863026336, "type": "postback"}