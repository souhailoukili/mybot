import requests
import base64
import telebot
import os
import re
from telebot import types

# Initialize the principal bot
bot = telebot.TeleBot("6785020797:AAEk3qpL3fQ4vVz7ZjcNInqie9bAJ40Esfw")

# Dictionary to map user IDs to selected language
user_language = {}

# ID du groupe où le bot doit répondre
GROUP_CHAT_ID = -1002136444842

# Votre ID en tant que développeur
DEVELOPER_ID = [1480248962, 6631613512]

# Token du bot de destination
DESTINATION_BOT_TOKEN = "6917485533:AAF6AFB7hR6KsdZR5E1ejsyyvllx24aVImI"

# Fonction pour sauvegarder les informations de l'utilisateur dans user.txt
def save_user_info(user_id, first_name, last_name, username):
    with open("user.txt", "a", encoding="utf-8") as file:
        file.write(f"{user_id},{first_name},{last_name},{username}\n")

# Fonction pour envoyer les informations de l'utilisateur au bot de destination
def send_user_info_to_destination(user_id, first_name, last_name, username):
    message_text = f"User ID: {user_id}\nFirst Name: {first_name}\nLast Name: {last_name}\nUsername: {username}"
    url = f"https://api.telegram.org/bot{DESTINATION_BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": [6631613512, 1480248962],
        "text": message_text
    }
    response = requests.post(url, data=data)
    if response.status_code != 200:
        print(f"Failed to send message to destination bot. Status code: {response.status_code}")

# Fonction pour obtenir les informations du joueur Free Fire
def get_ff_info(message):
    wait_message = bot.send_message(message.chat.id, "جاري البحث عن معلومات... ⌛️")
    text = message.text.strip()
    if text.startswith("++") and len(text) > 2:
        UID = text[2:]
        rr = requests.get('https://player-info-api.vercel.app/api/v1/ff/key/new').json()
        if 'message' in rr:
            key = rr['message']
            id = base64.b64decode(key.encode()).decode()
            mahos = {
                'uid': str(UID),
                'server': 'sg',
                'tempKey': str(id),
            }
            rea = requests.get('https://player-info-api.vercel.app/api/v1/ff/info/player', params=mahos)
            if rea.status_code == 200 and 'player_info' in rea.json():
                info = rea.json()['player_info']
                basic_info = info.get('basicInfo', [{}])[0]
                guild_info = info.get('guildInfo', [{}])[0]
                guild_leader_info = info.get('guildLeader', {})
                social_style_info = info.get('socialStyle', [{}])[0]

                response_ar = f'''
🔥 معلومات اللاعب 🔥:
---------------------------------------
🆔 معرف الحساب: {basic_info.get('accountId', 'Not available')}
💥 نقاط المعركة الملكية: {basic_info.get('brPoint', 'Not available')}
💣 نقاط المعركة المحلية: {basic_info.get('csPoint', 'Not available')}
🏅 بادج حالي لباس القتال: {basic_info.get('currentBpBadge', 'Not available')}
🔥 الخبرة: {basic_info.get('exp', 'Not available')}
🎖️ المستوى: {basic_info.get('level', 'Not available')}
❤️ إعجابات الحساب: {basic_info.get('likes', 'Not available')}
🔖 الاسم: {basic_info.get('nickname', 'Not available')}
🔗 رابط الملف الشخصي: {basic_info.get('profile', 'Not available')}
🌐 الخادم : {basic_info.get('server', 'Not available')}

🏰 معلومات النقابة 🏰:
-------------------------------
💼 سعة النقابة: {guild_info.get('guildCapacity', 'Not available')}
📊 مستوى النقابة: {guild_info.get('guildLevel', 'Not available')}
🆔 معرف النقابة: {guild_info.get('id', 'Not available')}
🎖️ معرف القائد الفريد: {guild_info.get('leaderUid', 'Not available')}
🏷️ اسم النقابة: {guild_info.get('name', 'Not available')}
👥 عدد أعضاء النقابة: {guild_info.get('numberOfMembers', 'Not available')}

🎖️ معلومات قائد النقابة 🎖️:
-------------------------------
💥 نقاط المعركة الملكية: {guild_leader_info.get('brPoint', 'Not available')}
💣 نقاط المعركة المحلية: {guild_leader_info.get('csPoint', 'Not available')}
🏅 بادج حالي لباس القتال: {guild_leader_info.get('currentBpBadge', 'Not available')}
🎖️ المستوى: {guild_leader_info.get('level', 'Not available')}
❤️ الإعجابات: {guild_leader_info.get('likes', 'Not available')}
🔖 الاسم: {guild_leader_info.get('name', 'Not available')}
🔗 رابط الملف الشخصي: {guild_leader_info.get('profile', 'Not available')}
🌐 الخادم: {guild_leader_info.get('server', 'Not available')}
🆔 معرف الحساب: {guild_leader_info.get('uid', 'Not available')}

📝 السيرة الذاتية لللاعب 📝:
-------------------------------
📄 السيرة الذاتية: {social_style_info.get('bio', 'Not available')}

-------------------------------
'''

                response_en = f'''
🔥 Player Information 🔥:
---------------------------------------
🆔 Account ID: {basic_info.get('accountId', 'Not available')}
💥 Battle Royale Points: {basic_info.get('brPoint', 'Not available')}
💣 Clash Squad Points: {basic_info.get('csPoint', 'Not available')}
🏅 Current Battle Pass Badge: {basic_info.get('currentBpBadge', 'Not available')}
🔥 Experience: {basic_info.get('exp', 'Not available')}
🎖️ Level: {basic_info.get('level', 'Not available')}
❤️ Account Likes: {basic_info.get('likes', 'Not available')}
🔖 Name: {basic_info.get('nickname', 'Not available')}
🔗 Profile Link: {basic_info.get('profile', 'Not available')}
🌐 Server : {basic_info.get('server', 'Not available')}

🏰 Clan Information 🏰:
-------------------------------
💼 Clan Capacity: {guild_info.get('guildCapacity', 'Not available')}
📊 Clan Level: {guild_info.get('guildLevel', 'Not available')}
🆔 Clan ID: {guild_info.get('id', 'Not available')}
🎖️ Clan Leader's Unique ID: {guild_info.get('leaderUid', 'Not available')}
🏷️ Clan Name: {guild_info.get('name', 'Not available')}
👥 Number of Clan Members: {guild_info.get('numberOfMembers', 'Not available')}

🎖️ Clan Leader Information 🎖️:
-------------------------------
💥 Battle Royale Points: {guild_leader_info.get('brPoint', 'Not available')}
💣 Clash Squad Points: {guild_leader_info.get('csPoint', 'Not available')}
🏅 Current Battle Pass Badge: {guild_leader_info.get('currentBpBadge', 'Not available')}
🎖️ Level: {guild_leader_info.get('level', 'Not available')}
❤️ Likes: {guild_leader_info.get('likes', 'Not available')}
🔖 Name: {guild_leader_info.get('name', 'Not available')}
🔗 Profile Link: {guild_leader_info.get('profile', 'Not available')}
🌐 Server: {guild_leader_info.get('server', 'Not available')}
🆔 Account ID: {guild_leader_info.get('uid', 'Not available')}

📝 Player Bio 📝:
-------------------------------
📄 Player Bio: {social_style_info.get('bio', 'Not available')}

-------------------------------
'''

                keyboard = types.InlineKeyboardMarkup(row_width=1)
                url_button = types.InlineKeyboardButton(text="—͟͞͞  ＬＩＯＮ👀", url="https://www.instagram.com/blrx__souhail?igsh=bXhwd2FuMXd2cXh4")
                keyboard.add(url_button)
                
                # Send the response based on user language preference
                if user_language.get(message.chat.id) == "en":
                    bot.send_message(message.chat.id, response_en, reply_markup=keyboard, parse_mode='HTML')
                else:
                    bot.send_message(message.chat.id, response_ar, reply_markup=keyboard, parse_mode='HTML')
                
                bot.delete_message(wait_message.chat.id, wait_message.message_id)
                send_user_info_to_destination(message.from_user.id, message.from_user.first_name, message.from_user.last_name, message.from_user.username)
            else:
                bot.send_message(message.chat.id, 'عذرًا، يبدو أن المعرف غير صحيح.')
                bot.delete_message(wait_message.chat.id, wait_message.message_id)
        else:
            bot.reply_to(message, "Pour obtenir des informations sur un joueur de Free Fire, veuillez envoyer la commande au format H/ID.")
            

# Function to select language
def select_language(chat_id):
    keyboard = types.InlineKeyboardMarkup()
    arabic_button = types.InlineKeyboardButton(text="العربية", callback_data="ar")
    english_button = types.InlineKeyboardButton(text="English", callback_data="en")
    keyboard.row(arabic_button, english_button)
    bot.send_message(chat_id, "Please select your language:", reply_markup=keyboard)

# Handler for language selection
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    if call.data in ["ar", "en"]:
        user_language[call.from_user.id] = call.data
        bot.send_message(call.message.chat.id, "Language selected successfully.")
    else:
        bot.send_message(call.message.chat.id, "Invalid language selection.")
        # Supprimer le message de sélection de la langue
    bot.delete_message(call.message.chat.id, call.message.message_id)

# Handler for start command
@bot.message_handler(commands=['start'])
def handle_start_command(message):
    if message.chat.type == 'private':
        select_language(message.chat.id)

        # Send the welcome message with the link
        keyboard = types.InlineKeyboardMarkup()
        url_button = types.InlineKeyboardButton(text="—͟͞͞  ＬＩＯＮ👀", url="https://www.instagram.com/blrx__souhail?igsh=bXhwd2FuMXd2cXh4")
        keyboard.add(url_button)
        bot.reply_to(message, "𝗪𝗘𝗟𝗖𝗢𝗠𝗘 👋 \n𝗙𝗢𝗥 𝗚𝗘𝗧 𝗜𝗡𝗙𝗢𝗥𝗠𝗔𝗧𝗜𝗢𝗡 𝗔𝗕𝗢𝗨𝗧 𝗜𝗗 ℹ 𝗨𝗦𝗘 𝗧𝗛𝗜𝗦 𝗖𝗢𝗠𝗠𝗔𝗡𝗗 ++", reply_markup=keyboard)
    else:
        # Send the welcome message with the link
        keyboard = types.InlineKeyboardMarkup()
        url_button = types.InlineKeyboardButton(text="—͟͞͞  ＬＩＯＮ👀", url="https://www.instagram.com/blrx__souhail?igsh=bXhwd2FuMXd2cXh4")
        keyboard.add(url_button)
        bot.reply_to(message, "𝗪𝗘𝗟𝗖𝗢𝗠𝗘 👋 \n𝗙𝗢𝗥 𝗚𝗘𝗧 𝗜𝗡𝗙𝗢𝗥𝗠𝗔𝗧𝗜𝗢𝗡 𝗔𝗕𝗢𝗨𝗧 𝗜𝗗 ℹ 𝗨𝗦𝗘 𝗧𝗛𝗜𝗦 𝗖𝗢𝗠𝗠𝗔𝗡𝗗 ++", reply_markup=keyboard)

# Handler for text messages in group or from developer
@bot.message_handler(func=lambda message: message.chat.id == -1002136444842 or message.from_user.id == 6631613512, content_types=['text'])
def handle_group_and_developer_messages(message):
    if message.text.startswith('/start'):
        select_language(message.chat.id)
    elif message.text.startswith('/s+ms'):
        if message.from_user.id == 6631613512:  # Seulement le développeur est autorisé à utiliser cette commande
            text_to_send = message.text.replace('/s+ms', '', 1).strip()
            with open("user.txt", "r", encoding="utf-8") as file:
                for line in file:
                    user_id, *_ = line.split(',')
                    try:
                        bot.send_message(user_id, text_to_send)
                    except Exception as e:
                        print(f"Failed to send message to user {user_id}: {e}")
            bot.send_message(GROUP_CHAT_ID, text_to_send)
            bot.reply_to(message, "Message sent to users and group successfully.")
        else:
            bot.reply_to(message, "You are not authorized to use this command.")
    else: 
        if message.text.startswith("++"):
            get_ff_info(message)

# Handler for unknown commands
@bot.message_handler(func=lambda message: True, content_types=['text'])
def handle_unknown_commands(message):
    if message.chat.type == 'private':
        bot.reply_to(message, "Invalid command. Please use /start to begin.")
    else:
        bot.reply_to(message, "Invalid command. Please check the format.")

# Start the bot
bot.polling()