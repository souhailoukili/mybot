import requests
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

# Replace with your actual Telegram bot API key
TELEGRAM_API_KEY = '7398587700:AAFt2GhEuo44o_ILmT7D3THmecAell8vuag'
bot = telebot.TeleBot(TELEGRAM_API_KEY)

user_language = {}
user_player_id = {}

def get_player_info(player_id):
    url = f'https://www.public.freefireinfo.site/api/info/sg/{player_id}?key=Ryz'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def create_info_image(avatar_url, banner_url, player_name, player_id, player_level):
    avatar_response = requests.get(avatar_url)
    banner_response = requests.get(banner_url)
    
    avatar_image = Image.open(BytesIO(avatar_response.content)).resize((150, 150))
    banner_image = Image.open(BytesIO(banner_response.content)).resize((450, 150))
    
    combined_image = Image.new('RGBA', (600, 150))
    combined_image.paste(avatar_image, (0, 0))
    combined_image.paste(banner_image, (150, 0))
    
    draw = ImageDraw.Draw(combined_image)
    font_large = ImageFont.truetype("/mnt/data/arial.ttf", 36)
    font_medium = ImageFont.truetype("/mnt/data/arial.ttf", 24)
    
    draw.text((160, 10), player_name, font=font_large, fill="white")
    draw.text((160, 90), f"ID: {player_id}", font=font_large, fill="white")
    draw.text((500, 110), f"Lv: {player_level}", font=font_medium, fill="white", anchor="ra")
    
    return combined_image

messages = {
    'en': {
        'enter_id': "🆔 Please enter the player ID:",
        'choose_language': "🌐 Please choose your language:",
        'language_set': "🇬🇧 Language set to English.",
        'player_info': (
            "ℹ️ Account Information:\n"
            "- 📛 Name: {Account Name}\n"
            "- 🆔 UID: {Account UID}\n"
            "- 📈 Level: {Account Level}\n"
            "- 👍 Likes: {Account Likes}\n"
            "- 🌍 Region: {Account Region}\n"
            "- 📝 Bio: {Account Signature}\n"
            "- 🕰️ Last Login: {Account Last Login (GMT 0530)}\n"
            "- 🎟️ Booyah Pass: {Account Booyah Pass}\n"
            "- 🏅 Booyah Pass Badges: {Account Booyah Pass Badges}\n"
            "- 📅 Create Time: {Account Create Time (GMT 0530)}\n"
            "- 💯 Honor Score: {Account Honor Score}\n"
            "- 🌐 Language: {Account Language}\n"
            "🐾 Pet Info:\n"
            "- 📈 Pet Level: {Pet Level}\n"
            "- 🐾 Pet Name: {Pet Name}\n"
            "- 🐶 Pet Type: {Pet Type}\n"
            "- 🔝 Pet XP: {Pet XP}\n"
            "🛡️ Guild Leader Info:\n"
            "- 🏰 Guild Capacity: {Guild Capacity}\n"
            "- 👥 Guild Current Members: {Guild Current Members}\n"
            "- 🆔 Guild ID: {Guild ID}\n"
            "- 📈 Guild Level: {Guild Level}\n"
            "- 📛 Guild Name: {Guild Name}\n"
            "- 🆔 Guild Leader ID: {Leader ID}\n"
            "- 🎖️ Guild Leader Title: {Leader Title}\n"
            "- 📍 Guild Leader Pin: {Leader Pin}\n"
            "- 🔝 Guild Leader XP: {Leader XP}\n"
        )
    },
    'ar': {
        'enter_id': "🆔 يرجى إدخال معرف اللاعب:",
        'choose_language': "🌐 يرجى اختيار لغتك:",
        'language_set': "🇸🇦 تم تعيين اللغة إلى العربية.",
        'player_info': (
            "ℹ️ معلومات الحساب:\n"
            "- 📛 الاسم: {Account Name}\n"
            "- 🆔 UID: {Account UID}\n"
            "- 📈 المستوى: {Account Level}\n"
            "- 👍 الإعجابات: {Account Likes}\n"
            "- 🌍 المنطقة: {Account Region}\n"
            "- 📝 السيرة الذاتية: {Account Signature}\n"
            "- 🕰️ آخر تسجيل دخول: {Account Last Login (GMT 0530)}\n"
            "- 🎟️ Booyah Pass: {Account Booyah Pass}\n"
            "- 🏅 شارات Booyah Pass: {Account Booyah Pass Badges}\n"
            "- 📅 وقت الإنشاء: {Account Create Time (GMT 0530)}\n"
            "- 💯 درجة الشرف: {Account Honor Score}\n"
            "- 🌐 اللغة: {Account Language}\n"
            "🐾 معلومات الحيوان الأليف:\n"
            "- 📈 مستوى الحيوان الأليف: {Pet Level}\n"
            "- 🐾 اسم الحيوان الأليف: {Pet Name}\n"
            "- 🐶 نوع الحيوان الأليف: {Pet Type}\n"
            "- 🔝 XP الحيوان الأليف: {Pet XP}\n"
            "🛡️ معلومات قائد النقابة:\n"
            "- 🏰 سعة النقابة: {Guild Capacity}\n"
            "- 👥 الأعضاء الحاليين للنقابة: {Guild Current Members}\n"
            "- 🆔 معرف النقابة: {Guild ID}\n"
            "- 📈 مستوى النقابة: {Guild Level}\n"
            "- 📛 اسم النقابة: {Guild Name}\n"
            "- 🆔 معرف قائد النقابة: {Leader ID}\n"
            "- 🎖️ لقب قائد النقابة: {Leader Title}\n"
            "- 📍 رمز قائد النقابة: {Leader Pin}\n"
            "- 🔝 XP قائد النقابة: {Leader XP}\n"
        )
    },
    'fr': {
        'enter_id': "🆔 Veuillez entrer l'ID du joueur:",
        'choose_language': "🌐 Veuillez choisir votre langue:",
        'language_set': "🇫🇷 La langue a été définie sur le français.",
        'player_info': (
            "ℹ️ Informations sur le compte:\n"
            "- 📛 Nom: {Account Name}\n"
            "- 🆔 UID: {Account UID}\n"
            "- 📈 Niveau: {Account Level}\n"
            "- 👍 J'aime: {Account Likes}\n"
            "- 🌍 Région: {Account Region}\n"
            "- 📝 Bio: {Account Signature}\n"
            "- 🕰️ Dernière connexion: {Account Last Login (GMT 0530)}\n"
            "- 🎟️ Booyah Pass: {Account Booyah Pass}\n"
            "- 🏅 Badges Booyah Pass: {Account Booyah Pass Badges}\n"
            "- 📅 Temps de création: {Account Create Time (GMT 0530)}\n"
            "- 💯 Score d'honneur: {Account Honor Score}\n"
            "- 🌐 Langue: {Account Language}\n"
            "🐾 Informations sur l'animal de compagnie:\n"
            "- 📈 Niveau de l'animal: {Pet Level}\n"
            "- 🐾 Nom de l'animal: {Pet Name}\n"
            "- 🐶 Type d'animal: {Pet Type}\n"
            "- 🔝 XP de l'animal: {Pet XP}\n"
            "🛡️ Informations sur le chef de guilde:\n"
            "- 🏰 Capacité de la guilde: {Guild Capacity}\n"
            "- 👥 Membres actuels de la guilde: {Guild Current Members}\n"
            "- 🆔 ID de la guilde: {Guild ID}\n"
            "- 📈 Niveau de la guilde: {Guild Level}\n"
            "- 📛 Nom de la guilde: {Guild Name}\n"
            "- 🆔 ID du chef de guilde: {Leader ID}\n"
            "- 🎖️ Titre du chef de guilde: {Leader Title}\n"
            "- 📍 Épinglette du chef de guilde: {Leader Pin}\n"
            "- 🔝 XP du chef de guilde: {Leader XP}\n"
        )
    }
}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "👋 Welcome! To get player information, type /get [player ID].")

@bot.message_handler(commands=['get'])
def get_player(message):
    try:
        player_id = message.text.split()[1]
        user_player_id[message.chat.id] = player_id
        markup = InlineKeyboardMarkup(row_width=2)
        markup.add(
            InlineKeyboardButton("English 🇬🇧", callback_data="language_en"),
            InlineKeyboardButton("العربية 🇸🇦", callback_data="language_ar"),
            InlineKeyboardButton("Français 🇫🇷", callback_data="language_fr")
        )
        
        bot.reply_to(message, messages['en']['choose_language'], reply_markup=markup)
    except IndexError:
        bot.reply_to(message, "⚠️ Please provide a valid player ID. Example: /get 123456789")

@bot.callback_query_handler(func=lambda call: call.data.startswith("language_"))
def callback_language(call):
    lang = call.data.split("_")[1]
    user_language[call.message.chat.id] = lang

    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None)

    if lang == 'en':
        bot.send_message(call.message.chat.id, messages['en']['language_set'])
    elif lang == 'ar':
        bot.send_message(call.message.chat.id, messages['ar']['language_set'])
    elif lang == 'fr':
        bot.send_message(call.message.chat.id, messages['fr']['language_set'])

    player_id = user_player_id[call.message.chat.id]
    
    # Send a loading message with the search emoji
    loading_message = bot.send_message(call.message.chat.id, "🤖")

    player_info = get_player_info(player_id)
    
    if player_info:
        player_name = player_info.get('Account Name', 'N/A')
        player_level = player_info.get('Account Level', 'N/A')
        avatar_url = player_info.get('Account Avatar Image')
        banner_url = player_info.get('Account Banner Image')
        
        info_image = create_info_image(avatar_url, banner_url, player_name, player_id, player_level)
        
        info_bio = BytesIO()
        info_image.save(info_bio, format='PNG')
        info_bio.seek(0)
        
        # Sending the image as a photo to ensure it's non-empty
        bot.send_photo(call.message.chat.id, photo=info_bio)
        
        lang_messages = messages[lang]
        reply = lang_messages['player_info'].format(
            **player_info,
            **player_info.get('Equipped Pet Information', {}),
            **player_info.get('Guild Information', {}),
            **player_info.get('Guild Leader Information', {})
        )
    else:
        reply = "❌ Failed to retrieve data."

    # Edit the loading message with the actual information
    bot.edit_message_text(reply, call.message.chat.id, loading_message.message_id)

bot.polling()
