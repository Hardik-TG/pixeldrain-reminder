import json, time, datetime, os, threading
from telegram import Bot
from telegram.ext import Updater, MessageHandler, Filters

# === EDIT THIS PART ONLY ===
BOT_TOKEN = "7809884802:AAF2LSNQ2CcZ-Q7vqxqE0h-1dauI3807lKo"  # Paste your token here
CHAT_ID = "674591941"      # Paste your chat ID here
# ============================

DATA_FILE = "data.json"
bot = Bot(token=BOT_TOKEN)

def load_data():
    if not os.path.exists(DATA_FILE) or os.path.getsize(DATA_FILE) == 0:
        # create empty list if file missing or empty
        with open(DATA_FILE, "w") as f:
            json.dump([], f)
        return []
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

def add_file(link):
    data = load_data()
    data.append({"link": link, "date": str(datetime.date.today())})
    save_data(data)
    bot.send_message(chat_id=CHAT_ID, text=f"✅ Added link:\n{link}")

def check_reminders():
    while True:
        data = load_data()
        today = datetime.date.today()
        updated = []
        for item in data:
            upload_date = datetime.date.fromisoformat(item["date"])
            days_passed = (today - upload_date).days
            if days_passed == 113:
                bot.send_message(chat_id=CHAT_ID,
                                 text=f"⚠️ Reminder: Your Pixeldrain file will auto-delete in 7 days!\n{item['link']}")
            if days_passed < 120:
                updated.append(item)
        save_data(updated)
        time.sleep(86400)  # check daily

def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher
    def handle(update, context):
        text = update.message.text
        if "pixeldrain.com" in text:
            add_file(text)
        else:
            update.message.reply_text("Send a valid Pixeldrain link only!")
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle))
    threading.Thread(target=check_reminders, daemon=True).start()
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
