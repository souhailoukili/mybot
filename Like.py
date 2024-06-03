import logging
import requests
import concurrent.futures
import telebot
import datetime
from telebot import types
import time

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# API URL with player UID placeholder
api_url = "https://free-ff-api.onrender.com/api/v1/account?region=me&uid={uid}"

# Number of requests to send
number_of_requests = 50

# Function to send a request
def send_request(uid):
    try:
        response = requests.get(api_url.format(uid=uid))
        logger.info(f"Response Code: {response.status_code}, Response: {response.json()}")
    except Exception as e:
        logger.error(f"Error sending request: {e}")

# List of allowed chat IDs
allowed_chats = [-1002136444842, 6631613512]  # Replace these IDs with your group IDs

# Initialize the bot with your token
bot = telebot.TeleBot("7263112829:AAEEmqWJTFAuLhRsinRXtXoTbnktTG8CM-U")

# Start command handler
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, '''
🌟 مرحبا بك في بوت 🌟

🛠 لإرسال زوار:
👉 /SH
                 

ℹ️ لجلب معلومات:
👉 /HR
                 

ℹ️ لمعرفه حاله الحساب:
👉 /HS    


        🅱🅻🆁🆇 🅷🆁🅸🅶🅰
''')
    
    # Construire le clavier en ligne
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    url_button = types.InlineKeyboardButton(text="𝔹𝕃ℝ𝕏 𝕊𝕆𝕌ℍ𝔸𝕀𝕃❤️", url="https://www.instagram.com/blrx__souhail?igsh=bXhwd2FuMXd2cXh4")
    keyboard.add(url_button)
    url_button = types.InlineKeyboardButton(text="𝔹𝕃ℝ𝕏 ℍℝ𝕀𝔾𝔸❤️", url="https://www.instagram.com/blrx_hriga?igsh=MTJzMXBnYWtzd2FyNw==")
    keyboard.add(url_button)
            
    message_text = "Here is the developer information:"

            # Envoyer la réponse avec le clavier en ligne
    bot.send_message(message.chat.id, message_text, reply_markup=keyboard)

# Check if the chat is allowed
def is_allowed_chat(chat_id):
    return chat_id in allowed_chats

# Send visits command handler
@bot.message_handler(commands=['SH'])
def send_visits(message):
    chat_id = message.chat.id

    if is_allowed_chat(chat_id):
        try:
            uid = message.text.split()[1]
        except IndexError:
            bot.reply_to(message, 'يرجى توفير UID بعد الأمر /SH. 😊')
            return

        bot.reply_to(message, f'جاري إرسال {number_of_requests} طلبات باستخدام UID: {uid}')

        with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
            futures = [executor.submit(send_request, uid) for _ in range(number_of_requests)]
            for future in concurrent.futures.as_completed(futures):
                future.result()  # Capture potential exceptions from each thread

        bot.reply_to(message, "تم إرسال جميع الطلبات.")
    else:
        bot.reply_to(message, 'هذه المجموعة غير مسموح لها باستخدام هذا الأمر.')

# Function to get player info
def get_player_info(uid):
    response = requests.get(api_url.format(uid=uid))
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Player info command handler
@bot.message_handler(commands=['HR'])
def player_info(message):
    chat_id = message.chat.id

    if is_allowed_chat(chat_id):
        try:
            uid = message.text.split()[1]
        except IndexError:
            bot.reply_to(message, 'يرجى توفير UID بعد الأمر /HR.')
            return

        data = get_player_info(uid)
        if data:
            basic_info = data.get('basicInfo', {})
            captain_info = data.get('captainBasicInfo', {})
            clan_info = data.get('clanBasicInfo', {})
            credit_info = data.get('creditScoreInfo', {})
            pet_info = data.get('petInfo', {})
            profile_info = data.get('profileInfo', {})
            social_info = data.get('socialInfo', {})
            
            # Convert timestamp to human-readable format
            last_login_timestamp = int(basic_info.get('lastLoginAt', 0))
            last_login = datetime.datetime.fromtimestamp(last_login_timestamp).strftime('%b %d, %Y, %I:%M %p')

            created_at_timestamp = int(basic_info.get('createAt', 0))
            created_at = datetime.datetime.fromtimestamp(created_at_timestamp).strftime('%b %d, %Y, %I:%M %p')

            info = (
                f"┌ 📋 𝗔𝗰𝗰𝗼𝘂𝗻𝘁 𝗵𝗶𝘀𝘁𝗼𝗿𝘆  [×] \n"
                f"├─ Last Login : {last_login}\n"
                f"└─ Created At : {created_at}\n\n"

                f"┌ 👤 𝗔𝗰𝗰𝗼𝘂𝗻𝘁 𝗶𝗻𝗳𝗼𝗿𝗺𝗮𝘁𝗶𝗼𝗻 \n"
                f"├─ Account ID : {basic_info.get('accountId', 'N/A')}\n"
                f"├─ Nickname : {basic_info.get('nickname', 'N/A')}\n"
                f"├─ Level : {basic_info.get('level', 'N/A')}\n"
                f"├─ Likes : {basic_info.get('liked', 'N/A')}\n"
                f"├─ Experience : {basic_info.get('exp', 'N/A')}\n"
                f"├─ Avatar : {profile_info.get('avatarId', 'N/A')}\n"
                f"├─ Banner : {basic_info.get('title', 'N/A')}\n"
                f"├─ Rank : {basic_info.get('rank', 'N/A')}\n"
                f"├─ Ranking Points : {basic_info.get('rankingPoints', 'N/A')}\n"
                f"├─ Badge Count : {basic_info.get('badgeCnt', 'N/A')}\n"
                f"├─ Booyah Pass : {basic_info.get('hasElitePass', 'N/A')}\n"
                f"├─ CS Rank : {basic_info.get('csRank', 'N/A')}\n"
                f"├─ CS Ranking Points : {basic_info.get('csRankingPoints', 'N/A')}\n"
                f"└─ Bio : {social_info.get('signature', 'N/A')}\n\n"

                f"┌ 🛡️ 𝗚𝗨𝗜𝗟𝗗 𝗜𝗡𝗙𝗢 \n"
                f"├─ Clan ID : {clan_info.get('clanId', 'N/A')}\n"
                f"├─ Clan Name : {clan_info.get('clanName', 'N/A')}\n"
                f"├─ Level : {clan_info.get('clanLevel', 'N/A')}\n"
                f"├─ Capacity : {clan_info.get('capacity', 'N/A')}\n"
                f"├─ Member Num : {clan_info.get('memberNum', 'N/A')}\n"
                f"└─ Captain Name : {captain_info.get('nickname', 'N/A')}\n\n"

                f"┌ ♻️ 𝗚𝗨𝗜𝗟𝗗 𝗟𝗘𝗔𝗗𝗘𝗥 𝗜𝗡𝗙𝗢 \n"
                f"├─ Nickname : {captain_info.get('nickname', 'N/A')}\n"
                f"├─ Level : {captain_info.get('level', 'N/A')}\n"
                f"├─ Exp : {captain_info.get('exp', 'N/A')}\n"
                f"├─ Rank : {captain_info.get('rank', 'N/A')}\n"
                f"├─ Ranking Points : {captain_info.get('rankingPoints', 'N/A')}\n"
                f"├─ Badge Count : {captain_info.get('badgeCnt', 'N/A')}\n"
                f"├─ Likes : {captain_info.get('liked', 'N/A')}\n"
                f"├─ CS Rank : {captain_info.get('csRank', 'N/A')}\n"
                f"├─ CS Ranking Points : {captain_info.get('csRankingPoints', 'N/A')}\n"
                f"├─ Last Login At : {captain_info.get('lastLoginAt', 'N/A')}\n"
                f"└─ Created At : {captain_info.get('createAt','N/A')}\n\n"

                f"┌ 🐾 𝗣𝗘𝗧 𝗜𝗡𝗙𝗢 \n"
                f"├─ Pet ID : {pet_info.get('id', 'N/A')}\n"
                f"├─ Pet Name : {pet_info.get('name', 'N/A')}\n"
                f"├─ Pet Level : {pet_info.get('level', 'N/A')}\n"
                f"├─ Pet Experience : {pet_info.get('exp', 'N/A')}\n"
                f"└─ Selected Skill : {pet_info.get('selectedSkillId', 'N/A')}\n\n"

                f"┌ ⚙️ 𝗖𝗥𝗘𝗗𝗜𝗧 𝗦𝗖𝗢𝗥𝗘 𝗜𝗡𝗙𝗢 \n"
                f"├─ Credit Score : {credit_info.get('creditScore', 'N/A')}\n"
                f"├─ Reward State : {credit_info.get('rewardState', 'N/A')}\n"
                f"├─ Periodic Summary Likes : {credit_info.get('periodicSummaryLikeCnt', 'N/A')}\n"
                f"├─ Periodic Summary Illegal Actions : {credit_info.get('periodicSummaryIllegalCnt', 'N/A')}\n"
                f"└─ Periodic Summary End Time : {credit_info.get('periodicSummaryEndTime', 'N/A')}\n\n"
                
                f"🅱🅻🆁🆇 🅷🆁🅸🅶🅰 \n" 
            )

            bot.reply_to(message, info)
        else:
            bot.reply_to(message, "لم أتمكن من جلب المعلومات.")
    else:
        bot.reply_to(message, 'هذه المجموعة غير مسموح لها باستخدام هذا الأمر.')

@bot.message_handler(commands=['HS'])
def check_status_command(message):
    if message.from_user.id == allowed_chats or message.chat.id:
        if len(message.text.split()) == 2:
            player_id = message.text.split()[1]
        else:
            bot.reply_to(message, "𝐕𝐞𝐮𝐢𝐥𝐥𝐞𝐳 𝐟𝐨𝐮𝐫𝐧𝐢𝐫 𝐮𝐧𝐞 𝐜𝐨𝐦𝐦𝐚𝐧𝐝𝐞 𝐯𝐚𝐥𝐢𝐝𝐞 {𝐩𝐚𝐫 𝐞𝐱𝐞𝐦𝐩𝐥𝐞, /HS 𝟏𝟐𝟑𝟒𝟓𝟔𝟕𝟖}")
    else:
        bot.reply_to(message, "𝐕𝐨𝐮𝐬 𝐧'ê𝐭𝐞𝐬 𝐩𝐚𝐬 𝐚𝐮𝐭𝐨𝐫𝐢𝐬é à 𝐮𝐭𝐢𝐥𝐢𝐬𝐞𝐫 𝐜𝐞𝐭𝐭𝐞 𝐜𝐨𝐦𝐦𝐚𝐧𝐝𝐞 𝐝𝐚𝐧𝐬 𝐜𝐞 𝐠𝐫𝐨𝐮𝐩𝐞.")


    # Envoyer le message "recherche d'informations"
    searching_message = bot.reply_to(message, "Recherche des informations...")

    url = f"https://ff.garena.com/api/antihack/check_banned?lang=en&uid={player_id}"
    headers = {
        'User-Agent': "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
        'Accept': "application/json, text/plain, */*",
        'authority': "ff.garena.com",
        'accept-language': "en-GB,en-US;q=0.9,en;q=0.8",
        'referer': "https://ff.garena.com/en/support/",
        'sec-ch-ua': "\"Not_A Brand\";v=\"8\", \"Chromium\";v=\"120\"",
        'sec-ch-ua-mobile': "?1",
        'sec-ch-ua-platform': "\"Android\"",
        'sec-fetch-dest': "empty",
        'sec-fetch-mode': "cors",
        'sec-fetch-site': "same-origin",
        'x-requested-with': "B6FksShzIgjfrYImLpTsadjS86sddhFH",
        'Cookie': "_ga_8RFDT0P8N9=GS1.1.1706295767.2.0.1706295767.0.0.0; apple_state_key=8236785ac31b11ee960a621594e13693; datadome=bbC6XTzUAS0pXgvEs7uZOGJRMPj4wRJzOh2zJmrQaYViaPVLZOIi__jw~cnNaIU1FzrByJ_qVJa7MwmpH3Z2jjRxtDkzsy2hiDTQ4cPY_n0mAwB3seemjGYszNpsfteh; token_session=f40bfc2e69a573f3bdb597e03c81c41f9ecf255f69d086aac38061fc350315ba5d64968819fe750f19910a1313b8c19b; _ga_Y1QNJ6ZLV6=GS1.1.1707023329.1.1.1707023568.0.0.0; _ga_KE3SY7MRSD=GS1.1.1707023591.1.1.1707023591.0.0.0; _gid=GA1.2.1798904638.1707023592; _gat_gtag_UA_207309476_25=1; _ga_RF9R6YT614=GS1.1.1707023592.1.0.1707023592.0.0.0; _ga=GA1.1.925801730.1706287088"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        result = response.json()
        is_banned = result.get('data', {}).get('is_banned', 0)
        period = result.get('data', {}).get('period', 0)
        if is_banned == 1:
            message_text = f"𓅓 🅱🅻🆁🆇 🅷🆁🅸🅶🅰 𓅓\n\n"
            message_text += f"┏ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━\n"
            message_text += f"┃ 𒀽   ID du joueur : {player_id}\n"
            message_text += f"┣ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━\n"
            message_text += f"┃ 𒀽  Statut : Banni\n"
            message_text += f"┣ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━\n"
            message_text += f"┃ 𒀽   Durée : {period} jours\n"
            message_text += f"┗ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━\n"
            message_text += f" 💻𝘿𝙚𝙫𝙚𝙡𝙤𝙥𝙚𝙧: @lion_souhail\n"
        else:
            message_text = f"𓅓 🅱🅻🆁🆇 🅷🆁🅸🅶🅰 𓅓\n\n"
            message_text += f"┏ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━\n"
            message_text += f"┃ 𒀽   ID du joueur : {player_id}\n"
            message_text += f"┣ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━\n"
            message_text += f"┃ 𒀽  Statut : Non Banni\n"
            message_text += f"┗ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━\n"
            message_text += f" 💻𝘿𝙚𝙫𝙚𝙡𝙤𝙥𝙚𝙧: @lion_souhail\n"

        # Construire le clavier en ligne
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        url_button = types.InlineKeyboardButton(text="𝔹𝕃ℝ𝕏 𝕊𝕆𝕌ℍ𝔸𝕀𝕃❤️", url="https://www.instagram.com/blrx__souhail?igsh=bXhwd2FuMXd2cXh4")
        keyboard.add(url_button)
        url_button = types.InlineKeyboardButton(text="𝔹𝕃ℝ𝕏 ℍℝ𝕀𝔾𝔸❤️", url="https://www.instagram.com/blrx_hriga?igsh=MTJzMXBnYWtzd2FyNw==")
        keyboard.add(url_button)

        # Envoyer la réponse avec le clavier en ligne
        sent_message = bot.send_message(message.chat.id, message_text, reply_markup=keyboard)

        # Supprimer le message "recherche d'informations" après un délai (par exemple, 3 secondes)
        time.sleep(3)
        bot.delete_message(message.chat.id, searching_message.message_id)
    else:
        bot.reply_to(message, "𝐈𝐦𝐩𝐨𝐬𝐬𝐢𝐛𝐥𝐞 𝐝𝐞 𝐫é𝐜𝐮𝐩é𝐫𝐞𝐫 𝐥𝐞𝐬 𝐝𝐨𝐧𝐧é𝐞𝐬 𝐝𝐞𝐩𝐮𝐢𝐬 𝐥'𝐀𝐏𝐈")

        

# Start polling
bot.polling()
