import requests
import telebot
from telebot import types  # Importing types module for InlineKeyboardMarkup and InlineKeyboardButton

# Create a bot instance
bot = telebot.TeleBot("7159692211:AAGtEl_ElBe52TI2MF4mnI_kzf5L5H6MC0U")

# Define the group chat ID
group_chat_id = -1002136444842
# Define the developer's user ID
developer_user_id = 6631613512   

def process_input(message):
    try:
        input_parts = message.text.split()
        if len(input_parts) == 2 and input_parts[0].upper() == 'SH':
            uid = input_parts[1]

            bot.send_message(message.chat.id, "𝙍𝙚𝙘𝙝𝙚𝙧𝙘𝙝𝙚 𝙙𝙪 𝙟𝙤𝙪𝙚𝙪𝙧...⏳")
            # Creating the inline keyboard
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            url_button = types.InlineKeyboardButton(text="—͟͞͞  ＬＩＯＮ👀", url="https://www.instagram.com/blrx__souhail?igsh=bXhwd2FuMXd2cXh4")
            keyboard.add(url_button)

                # Sending the keyboard along with the message
            bot.send_message(message.chat.id, "𝗖𝗵𝗲𝗰𝗸 𝗼𝘂𝘁 𝗺𝘆 𝗜𝗻𝘀𝘁𝗮𝗴𝗿𝗮𝗺:", reply_markup=keyboard)

            v = 0
            num_visits = 100  # تحديث عدد الزيارات إلى 100
            success = True  # علم للدلالة على نجاح إرسال الزيارات
            visits_sent_message = ""  # الرسالة لتخزين إجمالي الزيارات المرسلة
            num_errors = 0
            num_success = 0
            while v < num_visits and success: 
                response = requests.get(f"https://freefireapi.com.br/api/search_id?id={uid}") 
                if response.status_code == 200: 
                    v += 1 
                    num_success += 1
                else: 
                    num_errors += 1
                    success = False  # تعيين العلم على False إذا حدث خطأ

            visits_sent_message = f"➪ : @{message.from_user.username}\n\n𝑨𝑳𝑳 𝑽𝑰𝑺𝑰𝑻𝑺 𝑯𝑨𝑽𝑬 𝑩𝑬𝑬𝑵 \n𝑺𝑬𝑵𝑻𖤐\n\n𓅓3 𝑺 𝑲 𝑹𖤍 - 𝑳𝑰𝑶𝑵 𝑺𝑶𝑼𝑯𝑨𝑰𝑳𓅓\n\n┏ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━\n┃ 💳 𝙐𝙄𝘿: {uid}\n┣ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━\n┃ 👀 𝙏𝙤𝙩𝙖𝙡 𝙫𝙞𝙨𝙞𝙩𝙨: {num_visits}\n┃ 🔴 𝙀𝙧𝙧𝙤𝙧: {num_errors}\n┃ 🟢 𝙎𝙪𝙘𝙘𝙚𝙨𝙨: {num_success}\n┣ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━\n┃ ✨ 𝙋𝙡𝙚𝙖𝙨𝙚 𝙧𝙚𝙨𝙩𝙖𝙧𝙩 𝙜𝙖𝙢𝙚 \n┃ 𝙖𝙣𝙙 𝙘𝙝𝙚𝙘𝙠 𝙫𝙞𝙨𝙞𝙩𝙨 ✨\n┗ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━\n  💻𝘿𝙚𝙫𝙚𝙡𝙤𝙥𝙚𝙧:\n @lion_souhail\n @MRX3SKR"

            # إرسال الرسالة بإجمالي الزيارات المرسلة
            bot.send_message(message.chat.id, visits_sent_message)
        else:
            bot.send_message(message.chat.id, "Invalid format. Please enter the input in the correct format: SH 12345678")
    except Exception as e:
        bot.send_message(message.chat.id, "Error processing input. Please try again.")

@bot.message_handler(func=lambda message: message.chat.id == group_chat_id or message.chat.id == developer_user_id)
def start(message):
    if message.text.startswith('SH'):
        process_input(message)

# تشغيل البوت
bot.polling()
