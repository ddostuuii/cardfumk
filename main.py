# -*- coding: utf-8 -*-
print("बॉट शुरू हो रहा है...")  # अब कोई एरर नहीं आएगा
import threading
import requests
import telebot
from telebot import types
from gatet import Tele  # Import the Tele function from gatet.py

# Bot configuration
TOKEN = "7972155010:AAEqGghoTd9msimu7KJ4oF8Gdx6GTdkn6uY"  # अपना बॉट टोकन डालें
CHANNEL_ID = -1002363906868  # आपके मुख्य चैनल का ID
CHANNEL_USERNAME = "seedhe_maut"  # आपके मुख्य चैनल का यूज़रनेम
SECOND_CHANNEL = "https://t.me/+sMppZZQt1G41MzU1"  # दूसरे चैनल का यूज़रनेम

bot = telebot.TeleBot(TOKEN, parse_mode="HTML")

# Global state
processing = {}
stop_processing = {}

# Function to check if user is a member of the main channel
def is_user_member(user_id):
    try:
        chat_member = bot.get_chat_member(CHANNEL_ID, user_id)
        return chat_member.status in ["member", "administrator", "creator"]
    except:
        return False  # अगर कोई error आए तो assume करेंगे कि यूज़र मेंबर नहीं है

# Handle /start command
@bot.message_handler(commands=["start"])
def start(message):
    user_id = message.from_user.id

    # अगर यूज़र मेंबर नहीं है, तो "Join Now" बटन दिखाएं
    if not is_user_member(user_id):
        keyboard = types.InlineKeyboardMarkup()
        join_button1 = types.InlineKeyboardButton("🚀 Join Main Channel", url=f"https://t.me/{CHANNEL_USERNAME}")
        join_button2 = types.InlineKeyboardButton("🔥 Join Second Channel", url=f"{SECOND_CHANNEL}")  # दूसरा चैनल
        check_button = types.InlineKeyboardButton("🔄 Check Again", callback_data="check_join")
        
        keyboard.add(join_button1)
        keyboard.add(join_button2)  # दूसरा चैनल का बटन ऐड किया
        keyboard.add(check_button)

        bot.send_message(
            message.chat.id,
            f"🔒 **Mass CC Checker**\n\n"
            f"🚀 **The Fastest & Most Secure CC Checker!**\n"
            f"💎 **Experience seamless & accurate checking like never before!**\n"
            f"👑 **Powered by:** [@seedhe_maut_bot](https://t.me/seedhe_maut_bot)\n\n"
            f"🌟 **Why Choose Us?**\n"
            f"✅ Ultra-fast & reliable checking\n"
            f"✅ Secure & private transactions\n"
            f"✅ 24/7 uptime with premium features\n\n"
            f"✨ To unlock full access, join our official channel:\n"
            f"👉 [Join Main Channel](https://t.me/{CHANNEL_USERNAME})\n"
            f"👉 [Join Second Channel]({SECOND_CHANNEL})\n\n"
            f"⚡ Once joined, use `/start` again and begin your journey!",
            reply_markup=keyboard,
            disable_web_page_preview=True,
        )
        return

    # बॉट का वेलकम मैसेज + पिक्चर
    bot.send_photo(
        message.chat.id,
        photo="https://t.me/seedhe_maut_owner9/35",
        caption="𝗖𝗰 𝗰𝗵𝗲𝗰𝗸𝗲𝗿 𝗯𝗼𝘁 𝗯𝘆 𝗠𝗮𝘂𝘁. 𝗨𝘀𝗲 𝗮𝗻𝗱 𝘀𝗲𝗻𝗱 𝗳𝗲𝗲𝗱𝗯𝗮𝗰𝗸!\n\n𝗦𝗲𝗻𝗱 𝗧𝗵𝗲 𝗙𝗶𝗹𝗲 𝗧𝗼 𝗖𝗵𝗲𝗰𝗸 ✔️"
    )



# Callback handler for "Check Again" button
@bot.callback_query_handler(func=lambda call: call.data == "check_join")
def check_join_status(call):
    user_id = call.from_user.id

    if is_user_member(user_id):
        bot.edit_message_text(
            "✅ अब आप चैनल में हैं! आप बॉट का इस्तेमाल कर सकते हैं।",
            chat_id=call.message.chat.id,
            message_id=call.message.message_id
        )
    else:
        keyboard = types.InlineKeyboardMarkup()
        join_button = types.InlineKeyboardButton("🚀 Join Now", url=f"https://t.me/{CHANNEL_USERNAME}")
        check_button = types.InlineKeyboardButton("🔄 Check Again", callback_data="check_join")
        keyboard.add(join_button)
        keyboard.add(check_button)

        bot.edit_message_text(
            "❌ आप अभी भी चैनल में नहीं हैं!\n\n"
            "👉 पहले [Join Now](https://t.me/{CHANNEL_USERNAME}) दबाएँ, फिर 'Check Again' दबाएँ।",
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=keyboard,
            disable_web_page_preview=True
        )

# Handle document upload
@bot.message_handler(content_types=["document"])
def handle_document(message):
    user_id = str(message.from_user.id)

    # Force join check
    if not is_user_member(user_id):
        keyboard = types.InlineKeyboardMarkup()
        join_button = types.InlineKeyboardButton("🚀 Join Now", url=f"https://t.me/{CHANNEL_USERNAME}")
        check_button = types.InlineKeyboardButton("🔄 Check Again", callback_data="check_join")
        keyboard.add(join_button)
        keyboard.add(check_button)

        bot.send_message(
            message.chat.id,
            f"🔒 **Access Denied!**\n\n"
            f"आपको पहले हमारे चैनल को जॉइन करना होगा:\n"
            f"👉 [Join Now](https://t.me/{CHANNEL_USERNAME})\n\n"
            f"⚡ फिर से `/start` कमांड यूज़ करें!",
            reply_markup=keyboard,
            disable_web_page_preview=True,
        )
        return

    if processing.get(user_id, False):
        bot.reply_to(message, "𝗣𝗹𝗲𝗮𝘀𝗲 𝘄𝗮𝗶𝘁! 𝗬𝗼𝘂𝗿 𝗽𝗿𝗲𝘃𝗶𝗼𝘂𝘀 𝗳𝗶𝗹𝗲 𝗶𝘀 𝘀𝘁𝗶𝗹𝗹 𝗯𝗲𝗶𝗻𝗴 𝗽𝗿𝗼𝗰𝗲𝘀𝘀𝗲𝗱. ⏳.")
        return

    processing[user_id] = True
    stop_processing[user_id] = False

    # Download the file
    file_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    file_path = f"combo_{user_id}.txt"
    with open(file_path, "wb") as file:
        file.write(downloaded_file)

    # Start processing
    ko = bot.reply_to(message, "𝘊𝘰𝘯𝘯𝘦𝘤𝘵𝘪𝘯𝘨 𝘕𝘦𝘵𝘸𝘰𝘳𝘬 𝘛𝘰 𝘊𝘩𝘦𝘤𝘬 𝘊𝘢𝘳𝘥𝘴.....⏳.").message_id
    threading.Thread(target=process_cards, args=(message, file_path, user_id, ko)).start()
def process_cards(message, file_path, user_id, ko):
    dd = 0
    ch = 0
    approved_cards = []
    declined_cards = []

    try:
        with open(file_path, "r") as file:
            lines = file.readlines()
            total = len(lines)

            for cc in lines:
                if stop_processing.get(user_id, False):
                    bot.send_message(message.chat.id, "🛑 𝙋𝙧𝙤𝙘𝙚𝙨𝙨𝙞𝙣𝙜 𝙎𝙩𝙤𝙥𝙥𝙚𝙙 𝙗𝙮 𝙐𝙨𝙚𝙧.")
                    break

                cc = cc.strip()

                # Process card using Tele function
                try:
                    last = str(Tele(cc))  # Use the Tele function from gatet.py
                except Exception as e:
                    print(e)
                    last = "Your card was declined."

                # Update counts based on response
                if "succeeded" in last:
                    ch += 1
                    approved_cards.append(cc)
                else:
                    dd += 1
                    declined_cards.append(cc)

                # Update the progress message
                mes = types.InlineKeyboardMarkup(row_width=1)
                cm1 = types.InlineKeyboardButton(f"• ➼ {cc} •", callback_data='u8')
                cm2 = types.InlineKeyboardButton(f"• 𝗔𝗽𝗽𝗿𝗼𝘃𝗲𝗱 ✅: [ {ch} ] •", callback_data='x')
                cm3 = types.InlineKeyboardButton(f"• 𝗗𝗲𝗮𝗱 ❌: [ {dd} ] •", callback_data='x')
                cm4 = types.InlineKeyboardButton(f"• 𝗧𝗼𝘁𝗮𝗹 💎: [ {total} ] •", callback_data='x')
                stop_btn = types.InlineKeyboardButton("[ 𝗦𝘁𝗼𝗽 🛑 ] ", callback_data='stop_process')
                mes.add(cm1, cm2, cm3, cm4, stop_btn)

                bot.edit_message_text(chat_id=message.chat.id, message_id=ko, text='''𝘾𝙃𝙀𝘾𝙆𝙄𝙉𝙂 𝙔𝙊𝙐𝙍 𝘾𝘼𝙍𝘿𝙎...''', reply_markup=mes)

        # Checking complete message
        bot.send_message(message.chat.id, "✅ Checking complete! Sending results...")

        # Send approved cards
        if approved_cards:
            approved_text = "\n".join(approved_cards)
            send_large_message(message.chat.id, f"🎉 **Approved Cards ✅**:\n\n<code>{approved_text}</code>")

        # Send declined cards
        if declined_cards:
            declined_text = "\n".join(declined_cards)
            send_large_message(message.chat.id, f"❌ **Declined Cards**:\n\n<code>{declined_text}</code>")

    except Exception as e:
        print(f"Error processing cards: {e}")
    finally:
        processing[user_id] = False
        stop_processing[user_id] = False


# Function to handle large messages
def send_large_message(chat_id, text):
    max_length = 4096  # Telegram message limit
    parts = [text[i:i+max_length] for i in range(0, len(text), max_length)]
    for part in parts:
        bot.send_message(chat_id, part, parse_mode="HTML")


# Start the bot
bot.polling(none_stop=True)
