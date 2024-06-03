import logging
import requests
import concurrent.futures
import telebot
import datetime
from telebot import types

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# API URL with player UID placeholder
api_url = "https://free-ff-api.onrender.com/api/v1/account?region=me&uid=711414121"

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
        

# Start polling
bot.polling()
