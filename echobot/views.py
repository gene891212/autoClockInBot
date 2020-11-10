# coding=utf-8
from django.shortcuts import render

# Create your views here.
import requests
import os
import pyimgur

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

CLIENT_ID = os.environ['IMGUR_CLIENT_ID']
line_bot_api = LineBotApi(os.environ['CHANNEL_ACCESS_TOKEN'])
handler = WebhookHandler(os.environ['CHANNEL_SECRET'])

line_bot_api.set_default_rich_menu(init_rich_menu())

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
    user_detail = UserInformation.objects.get(user_id=event.source.user_id)

    if event.postback.data == 'check':
        push_sticker_message(event, f'Hi, {user_detail.user_name}.\nLinebot is Online.', '11537', '52002746')
    elif event.postback.data == 'clockIn':
        # line_bot_api.push_message(
        #     event.source.user_id,
        #     tempConfirmTemplate()
        # )
        reply_message(event, 'ClockIn Now...')
        try:
            echo, img_path = ClockIn(event).clockIn(user_detail.email_account, user_detail.email_password)
        except NoSuchElementException as e:
            push_message(event, e)
        else:
            push_sticker_message(event, echo, '11537', '52002734')

            im = pyimgur.Imgur(CLIENT_ID)
            image = im.upload_image(img_path, title="Uploaded with PyImgur")
            line_bot_api.push_message(
                event.source.user_id,
                ImageSendMessage(
                    original_content_url=image.link,
                    preview_image_url=image.link
                )
            )
    else:
        pass

@handler.add(FollowEvent)
def handle_message(event):
    # print(event)
    profile = line_bot_api.get_profile(event.source.user_id)
    text = f'Hi Hi {profile.display_name}, I\'m writing your information into database. You can not reject.'
    push_sticker_message(event, text, '11537', '52002753')
    if event.source.user_id not in all_user_id:
        UserInformation(user_id=profile.user_id, user_name=profile.display_name).save()

