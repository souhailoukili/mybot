import requests
import telebot
from telebot import types  # Importing types module for InlineKeyboardMarkup and InlineKeyboardButton

# Create a bot instance
bot = telebot.TeleBot("7159692211:AAGtEl_ElBe52TI2MF4mnI_kzf5L5H6MC0U")

# Define the group chat ID
group_chat_id = -1002017761926
# Define the developer's user ID
developer_user_id = 6927323442,   

def process_input(message):
    try:
        input_parts = message.text.split()
        if len(input_parts) == 4 and input_parts[0].upper() == 'SH':
            uid = input_parts[1]
            region = input_parts[2].lower()

            bot.send_message(message.chat.id, "𝙍𝙚𝙘𝙝𝙚𝙧𝙘𝙝𝙚 𝙙𝙪 𝙟𝙤𝙪𝙚𝙪𝙧...⏳")

            response = requests.get(f"https://freefireapi.com.br/api/search_id?id={uid}&region={region}")

            if response.status_code == 200: 
                name = response.json()['basicInfo']['nickname']
                bot.send_message(message.chat.id, f"𝙁𝙤𝙪𝙣𝙙 𝙋𝙡𝙖𝙮𝙚𝙧: {name}")

                # Creating the inline keyboard
                keyboard = types.InlineKeyboardMarkup(row_width=1)
                url_button = types.InlineKeyboardButton(text="—͟͞͞  ＬＩＯＮ👀", url="https://www.instagram.com/blrx__souhail?igsh=bXhwd2FuMXd2cXh4")
                keyboard.add(url_button)

                # Sending the keyboard along with the message
                bot.send_message(message.chat.id, "𝗖𝗵𝗲𝗰𝗸 𝗼𝘂𝘁 𝗺𝘆 𝗜𝗻𝘀𝘁𝗮𝗴𝗿𝗮𝗺:", reply_markup=keyboard)
            else: 
                bot.send_message(message.chat.id, f"Player Not Found, Status Code: {response.status_code}")
                return

            v = 0
            num_visits = 100
            success = True  # Flag to indicate whether visits were sent successfully
            visits_sent_message = ""  # Message to store the total visits sent
            num_errors = 0
            num_success = 0
            while v < num_visits and success: 
                response = requests.get(f"https://freefireapi.com.br/api/search_id?id={uid}&region={region}") 
                if response.status_code == 200: 
                    v += 1 
                    num_success += 1
                else: 
                    num_errors += 1
                    success = False  # Set flag to False if an error occurs

            visits_sent_message = f"𝐀𝐥𝐥 𝐯𝐢𝐬𝐢𝐭𝐬 𝐡𝐚𝐯𝐞 𝐛𝐞𝐞𝐧 𝐬𝐞𝐧𝐭!\n\n🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹\n┃ 💳 𝙐𝙄𝘿: {uid}\n🔸🔸🔸🔸🔸🔸🔸🔸🔸🔸🔸🔸🔸\n┃ 👀 𝙏𝙤𝙩𝙖𝙡 𝙫𝙞𝙨𝙞𝙩𝙨: {num_visits}\n┃ 🔴 𝙀𝙧𝙧𝙤𝙧: {num_errors}\n┃ 🟢 𝙎𝙪𝙘𝙘𝙚𝙨𝙨: {num_success}\n🔸🔸🔸🔸🔸🔸🔸🔸🔸🔸🔸🔸🔸\n┃ ✨ 𝙋𝙡𝙚𝙖𝙨𝙚 𝙧𝙚𝙨𝙩𝙖𝙧𝙩 𝙜𝙖𝙢𝙚 \n┃ 𝙖𝙣𝙙 𝙘𝙝𝙚𝙘𝙠 𝙫𝙞𝙨𝙞𝙩𝙨 ✨\n🔸🔸🔸🔸🔸🔸🔸🔸🔸🔸🔸🔸🔸\n┃ 💻 𝘿𝙚𝙫𝙚𝙡𝙤𝙥𝙚𝙧: \n@lion_souhail\n@MRX3SKR\n🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹"

            

            # Send the message with the total visits sent
            bot.send_message(message.chat.id, visits_sent_message)
        else:
            bot.send_message(message.chat.id, "Invalid format. Please enter the input in the correct format: SH 12345678 sg/ عدد المشاهدات الذي تريده")
    except Exception as e:
        bot.send_message(message.chat.id, "Error processing input. Please try again.")

@bot.message_handler(func=lambda message: message.chat.id == group_chat_id or message.chat.id == developer_user_id)
def start(message):
    if message.text.startswith('SH'):
        process_input(message)

# Run the bot
bot.polling()
