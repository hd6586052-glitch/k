import telebot
import requests
import SignerPy
import json
import secrets
import uuid
import datetime
import binascii
import os
import time
import random
import re
from bs4 import BeautifulSoup
import threading
from telebot import types


API_TOKEN = '8086016206:AAEj72-s17zHrCY5ZsDgaZVNE5Jh11a3_Wk'
bot = telebot.TeleBot(API_TOKEN)
CHANNEL_USERNAME = '@V_ii5'

CHANNEL_URL = 'https://t.me/V_ii5'

ADMIN_USER_ID = None 

print("اذهب الى البوت و اضغط /start")


def xor(string):
    return "".join([hex(ord(c) ^ 5)[2:] for c in string])


def check_subscription(user_id):
    try:
        chat_member = bot.get_chat_member(CHANNEL_USERNAME, user_id)
        if chat_member.status in ['member', 'administrator', 'creator']:
            return True
        return False
    except Exception as e:
        print(f"Error checking subscription: {e}")
        return False


def process_email(email, chat_id, message_id):
    try:
        msg = bot.send_message(chat_id, "الرجاء الانتظار...")
        secret = secrets.token_hex(16)
        xor_email = xor(email)
        
        # Request parameters
        params = {
            "request_tag_from": "h5",
            "fixed_mix_mode": "1",
            "mix_mode": "1",
            "account_param": xor_email,
            "scene": "1",
            "device_platform": "android",
            "os": "android",
            "ssmix": "a",
            "type": "3736",
            "_rticket": str(round(random.uniform(1.2, 1.6) * 100000000) * -1) + "4632",
            "cdid": str(uuid.uuid4()),
            "channel": "googleplay",
            "aid": "1233",
            "app_name": "musical_ly",
            "version_code": "370805",
            "version_name": "37.8.5",
            "manifest_version_code": "2023708050",
            "update_version_code": "2023708050",
            "ab_version": "37.8.5",
            "resolution": "1600*900",
            "dpi": "240",
            "device_type": "SM-G998B",
            "device_brand": "samsung",
            "language": "en",
            "os_api": "28",
            "os_version": "9",
            "ac": "wifi",
            "is_pad": "0",
            "current_region": "TW",
            "app_type": "normal",
            "sys_region": "US",
            "last_install_time": "1754073240",
            "mcc_mnc": "46692",
            "timezone_name": "Asia/Baghdad",
            "carrier_region_v2": "466",
            "residence": "TW",
            "app_language": "en",
            "carrier_region": "TW",
            "timezone_offset": "10800",
            "host_abi": "arm64-v8a",
            "locale": "en-GB",
            "ac2": "wifi",
            "uoo": "1",
            "op_region": "TW",
            "build_number": "37.8.5",
            "region": "GB",
            "ts": str(round(random.uniform(1.2, 1.6) * 100000000) * -1),
            "iid": str(random.randint(1, 10**19)),
            "device_id": str(random.randint(1, 10**19)),
            "openudid": str(binascii.hexlify(os.urandom(8)).decode()),
            "support_webview": "1",
            "okhttp_version": "4.2.210.6-tiktok",
            "use_store_region_cookie": "1",
            "app_version": "37.8.5"
        }
        
        cookies = {
            "passport_csrf_token": secret,
            "passport_csrf_token_default": secret,
            "install_id": params["iid"],
        }

        s = requests.session()

        # Get temporary email
        url_get_email = "https://www.guerrillamail.com/ajax.php?f=get_email_address"
        response = requests.get(url_get_email)
        data = response.json()
        name = data['email_addr']
        sid_token = data['sid_token']
        cookies = {'PHPSESSID': sid_token}
        s.cookies.update(cookies)

        # Sign and make initial request
        H = SignerPy.sign(params=params, cookie=cookies)
        headers = {
            'User-Agent': "com.zhiliaoapp.musically/2023708050 (Linux; U; Android 9; en_GB; SM-G998B; Build/SP1A.210812.016;tt-ok/3.12.13.16)",
            'x-ss-stub': H['x-ss-stub'],
            'x-tt-dm-status': "login=1;ct=1;rt=1",
            'x-ss-req-ticket': H['x-ss-req-ticket'],
            'x-ladon': H['x-ladon'],
            'x-khronos': H['x-khronos'],
            'x-argus': H['x-argus'],
            'x-gorgon': H['x-gorgon'],
            'content-type': "application/x-www-form-urlencoded",
            'content-length': H['content-length'],
        }

        url = "https://api16-normal-c-alisg.tiktokv.com/passport/account_lookup/email/"
        response = requests.post(url, headers=headers, params=params, cookies=cookies)
        print(response.text)
        passport_ticket = response.json()["data"]["accounts"][0]["passport_ticket"]

        # Send verification code
        name_xor = xor(name)
        url = "https://api16-normal-c-alisg.tiktokv.com/passport/email/send_code/"
        params.update({"not_login_ticket": passport_ticket, "email": name_xor})
        H = SignerPy.sign(params=params, cookie=cookies)
        headers = {
            'User-Agent': "com.zhiliaoapp.musically/2023708050 (Linux; U; Android 9; en_GB; SM-G998B; Build/SP1A.210812.016;tt-ok/3.12.13.16)",
            'Accept-Encoding': "gzip",
            'x-ss-stub': H['x-ss-stub'],
            'x-ss-req-ticket': H['x-ss-req-ticket'],
            'x-ladon': H['x-ladon'],
            'x-khronos': H['x-khronos'],
            'x-argus': H['x-argus'],
            'x-gorgon': H['x-gorgon'],
        }
        response = s.post(url, headers=headers, params=params, cookies=cookies)

        # Check for verification email
        time.sleep(5)
        last_email_id = None

        while True:
            url_check_email = "https://www.guerrillamail.com/ajax.php"
            params_check = {'f': 'check_email', 'seq': '0'}
            response = requests.get(url_check_email, params=params_check, cookies=cookies)
            emails = response.json().get('list', [])

            if emails:
                latest_email = emails[0]
                latest_email_id = latest_email['mail_id']

                if latest_email_id != last_email_id:
                    last_email_id = latest_email_id
                    mail_id = latest_email['mail_id']
                    url_fetch_email = f"https://www.guerrillamail.com/ajax.php?f=fetch_email&email_id={mail_id}"
                    email_response = requests.get(url_fetch_email, cookies=cookies)
                    email_content = email_response.json().get('mail_body', 'No Content')
                    soup = BeautifulSoup(email_content, "html.parser")
                    clean_text = soup.get_text()
                    match = re.search(r'This email was generated for\s+([\w\.]+)\.', clean_text)
                    if match:
                        username = match.group(1)
                        break

        # Get TikTok account info
        patre = {
            "Host": "www.tiktok.com",
            "sec-ch-ua": "\" Not A;Brand\";v=\"99\", \"Chromium\";v=\"99\", \"Google Chrome\";v=\"99\"",
            "sec-ch-ua-mobile": "?1",
            "sec-ch-ua-platform": "\"Android\"",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Linux; Android 8.0.0; Plume L2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.88 Mobile Safari/537.36",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "sec-fetch-site": "none",
            "sec-fetch-mode": "navigate",
            "sec-fetch-user": "?1",
            "sec-fetch-dest": "document",
            "accept-language": "en-US,en;q=0.9,ar-DZ;q=0.8,ar;q=0.7,fr;q=0.6,hu;q=0.5,zh-CN;q=0.4,zh;q=0.3"
        }
        url = f'https://www.tiktok.com/@{username}'
        tikinfo = requests.get(url, headers=patre).text

        try:
            getting = tikinfo.split('webapp.user-detail"')[1].split('"RecommendUserList"')[0]
            id = getting.split('id":"')[1].split('",')[0]
            name_tk = getting.split('nickname":"')[1].split('",')[0]
            bio = getting.split('signature":"')[1].split('",')[0]
            country = getting.split('region":"')[1].split('",')[0]
            private = "نعم" if getting.split('privateAccount":')[1].split(',"')[0] == "true" else "لا"
            followers = getting.split('followerCount":')[1].split(',"')[0]
            following = getting.split('followingCount":')[1].split(',"')[0]
            like = getting.split('heart":')[1].split(',"')[0]
            video = getting.split('videoCount":')[1].split(',"')[0]
            level = getting.split('userLevel":')[1].split(',"')[0] if 'userLevel"' in getting else "0"

            B = bin(int(id))[2:]
            BS = B[:31]
            Date = datetime.datetime.fromtimestamp(int(BS, 2)).strftime('%Y')

            result = (
                f"・═════ TikTok  ═════・\n"
                f"🧃 Username : {username}\n"
                f"🧃 Email : {email}\n"
                f"🧃 Followers : {followers}\n"
                f"🧃 Likes : {like}\n"
                f"🧃 Video : {video}\n"
                f"🧃 private : {private}\n"
                f"🧃 level : {level}\n"
                f"🧃 Date : {Date}\n"
                f"🧃 Dev : @Xiil6\n"
                f"・═════  EAN  ═════・\n"
            )

            bot.edit_message_text(result, chat_id, msg.message_id)

        except Exception as e:
            bot.edit_message_text("خطأ في استخراج اسم المستخدم، حاول مرة أخرى لاحقًا", chat_id, msg.message_id)

    except Exception as e:
        try:
            bot.edit_message_text("خطأ في استخراج اسم المستخدم، حاول مرة أخرى لاحقًا", chat_id, msg.message_id)
        except:
            pass

# Bot handlers
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    user_id = message.from_user.id
    if not check_subscription(user_id):
        # إنشاء زر للانضمام إلى القناة
        keyboard = types.InlineKeyboardMarkup()
        channel_button = types.InlineKeyboardButton(text="انضم إلى القناة", url=CHANNEL_URL)
        check_button = types.InlineKeyboardButton(text="تحقق من الاشتراك", callback_data="check_subscription")
        keyboard.add(channel_button, check_button)
        
        bot.send_message(user_id, f"عذراً، يجب عليك الانضمام إلى القناة أولاً:\n{CHANNEL_URL}", reply_markup=keyboard)
        return
    
    bot.reply_to(message, "مرحباً! ارسل الايميل لفحص المتاح")

@bot.callback_query_handler(func=lambda call: call.data == "check_subscription")
def check_subscription_callback(call):
    user_id = call.from_user.id
    if check_subscription(user_id):
        bot.edit_message_text("شكراً لك على الاشتراك! الآن يمكنك استخدام البوت.", user_id, call.message.message_id)
        bot.send_message(user_id, "ارسل الايميل لفحص المتاح")
    else:
        bot.answer_callback_query(call.id, "لم تنضم بعد إلى القناة. يرجى الانضمام أولاً.", show_alert=True)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_id = message.from_user.id
    if not check_subscription(user_id):
        
        keyboard = types.InlineKeyboardMarkup()
        channel_button = types.InlineKeyboardButton(text="انضم إلى القناة", url=CHANNEL_URL)
        check_button = types.InlineKeyboardButton(text="تحقق من الاشتراك", callback_data="check_subscription")
        keyboard.add(channel_button, check_button)
        
        bot.send_message(user_id, f"عذراً، يجب عليك الانضمام إلى القناة أولاً:\n{CHANNEL_URL}", reply_markup=keyboard)
        return
    
    email = message.text.strip()
    threading.Thread(target=process_email, args=(email, user_id, message.message_id)).start()

bot.polling(none_stop=True)