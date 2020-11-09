from linebot.models import *
from linebot import LineBotApi

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

import time
import re
import os

import pyimgur

CLIENT_ID = os.environ['IMGUR_CLIENT_ID']
line_bot_api = LineBotApi(os.environ['CHANNEL_ACCESS_TOKEN'])


class ClockIn():
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    # chrome_options.add_argument('--start-maximized')  # for windows
    # chrome_options.add_argument('--kiosk')            # for linux or mac
    def __init__(self, event):
        self.event = event

    def clockIn(self, account, password):
        def confirmUrl(url):
            while(chrome.current_url != url):
                pass
            time.sleep(3)
        def get_screenshot():
            localtime = time.strftime('%Y-%m-%d_%H-%M-%S')
            img_path = f'img/{localtime}.png'
            chrome.save_screenshot(img_path)
            im = pyimgur.Imgur(CLIENT_ID)
            image = im.upload_image(img_path, title="Uploaded with PyImgur")
            return image.link

        chrome = webdriver.Remote(
            command_executor='http://127.0.0.1:4444/wd/hub',
            desired_capabilities=DesiredCapabilities.CHROME
        )
        # chrome = webdriver.Chrome('./chromedriver', chrome_options=self.chrome_options)
        
        chrome.get("https://dpqqa.com")
        # login by microsoft
        confirmUrl('https://dpqqa.com/authentication/login')
        chrome.find_element_by_xpath('/html/body/app-root/app-login/div/div[2]/div/div/button[1]').click()
        push_message(self.event, 'Login Microsoft account now. Please wait for your confirmation...')
        time.sleep(8)

        # account and password
        chrome.switch_to_window(chrome.window_handles[1])
        chrome.find_element_by_id('i0116').send_keys(account)
        chrome.find_element_by_id('idSIButton9').click()
        time.sleep(2)
        chrome.find_element_by_id('i0118').send_keys(password)
        chrome.find_element_by_id('idSIButton9').click()

        # confirm
        confirmUrl('https://login.microsoftonline.com/common/SAS/ProcessAuth')
        chrome.find_element_by_id('idSIButton9').click()
        time.sleep(3)

        # clock in button
        chrome.switch_to_window(chrome.window_handles[0])
        time.sleep(1)
        confirmUrl('https://dpqqa.com/')
        chrome.find_element_by_xpath('/html/body/app-root/app-header/mat-toolbar/div[2]/button[4]').click()

        # clock in
        # confirmUrl(re.search(r'https://dpqqa.com/clock/\d+', chrome.current_url).group())
        # chrome.find_element_by_xpath('/html/body/app-root/app-clock/div/div/div[1]/div/button[1]').click()
        time.sleep(3)

        image_link = get_screenshot()
        local_time = chrome.find_element_by_xpath('/html/body/app-root/app-clock/div/div/div[2]/div/table/tbody/tr[1]/td[1]').text
        status = chrome.find_element_by_xpath('/html/body/app-root/app-clock/div/div/div[2]/div/table/tbody/tr[1]/td[2]').text
        account_name = chrome.find_element_by_xpath('//html/body/app-root/app-header/mat-toolbar/div[4]/button/span').text
        
        chrome.close()
        return f'{account_name}\nThe Lastest:\n{local_time} ({status})', image_link

# rich menu
def init_rich_menu():
    rich_menu_to_create = RichMenu(
        size=RichMenuSize(width=2500, height=750),
        selected=False,
        name="Nice richmenu",
        chat_bar_text="Tap here",
        areas=[
            RichMenuArea(
                bounds=RichMenuBounds(x=0, y=0, width=1250, height=750),
                action=PostbackAction(
                    display_text='Test Linebot Online',
                    data='check'
                )
            ),
            RichMenuArea(
                bounds=RichMenuBounds(x=1250, y=0, width=1250, height=750),
                action=PostbackAction(
                    display_text='Clock In',
                    data='clockIn'
                )
            )
        ]
    )
    rich_menu_id = line_bot_api.create_rich_menu(rich_menu=rich_menu_to_create)
    with open('richmenu.png', 'rb') as f:
        line_bot_api.set_rich_menu_image(rich_menu_id, 'image/png', f)
    return rich_menu_id


def push_message(event, text):
    line_bot_api.push_message(
        event.source.user_id,
        TextSendMessage(text=text)
    )

def push_sticker_message(event, text, package_id, sticker_id):
    line_bot_api.push_message(
        event.source.user_id,
        messages=[
            TextSendMessage(text=text),
            StickerSendMessage(
                package_id=package_id,
                sticker_id=sticker_id
            )
        ]
    )
def reply_message(event, text):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=text)
    )

# Message Type
def tempConfirmTemplate():
    confirm_template_message = TemplateSendMessage(
        alt_text='Confirm template',
        template=ConfirmTemplate(
            text='Are you sure?',
            actions=[
                PostbackAction(
                    label='postback',
                    display_text='postback text',
                    data='action=buy&itemid=1'
                ),
                MessageAction(
                    label='message',
                    text='message text'
                )
            ]
        )
    )
    return confirm_template_message

def tempQuickReply(event):
    text_message = TextSendMessage(
        text=event.message.text,
        quick_reply=QuickReply(
            items=[
                QuickReplyButton(action=MessageAction(label="label", text="text1")),
                QuickReplyButton(action=MessageAction(label="label2", text="text2"))
            ]
        )
    )
    return text_message

def tempLocation():
    location_message = LocationSendMessage(
        title='my location',
        address='Tokyo',
        latitude=24.431816,
        longitude=121.403623
    )
    return location_message
## Template
def tempButtonTemplate():
    buttons_template_message = TemplateSendMessage(
        alt_text='Buttons template',
        template=ButtonsTemplate(
            thumbnail_image_url='https://raw.githubusercontent.com/gene891212/test/master/about_pic.png',
            title='Menu',
            text='Please select',
            actions=[
                PostbackAction(
                    label='postback',
                    display_text='postback text',
                    data='action=buy&itemid=1'
                ),
                MessageAction(
                    label='message',
                    text='message text'
                ),
                URIAction(
                    label='uri',
                    uri='https://github.com/line/line-bot-sdk-python'
                )
            ]
        )
    )
    return buttons_template_message



def tempCarouselTemplate():
    image_carousel_template_message = TemplateSendMessage(
        alt_text='ImageCarousel template',
        template=ImageCarouselTemplate(
            columns=[
                ImageCarouselColumn(
                    image_url='https://raw.githubusercontent.com/gene891212/test/master/after-mask_pc.png',
                    action=PostbackAction(
                        label='postback1',
                        display_text='postback text1',
                        data='action=buy&itemid=1'
                    )
                ),
                ImageCarouselColumn(
                    image_url='https://raw.githubusercontent.com/gene891212/test/master/after-deemo.png',
                    action=PostbackAction(
                        label='postback2',
                        display_text='postback text2',
                        data='action=buy&itemid=2'
                    )
                )
            ]
        )
    )
    return image_carousel_template_message