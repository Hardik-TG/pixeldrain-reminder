import json, os, datetime, threading, time
from telegram import Bot, Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

BOT_TOKEN = "7809884802:AAF2LSNQ2CcZ-Q7vqxqE0h-1dauI3807lKo"
CHAT_ID = "674591941"
DATA_FILE = "data.json"

bot = Bot(token=BOT_TOKEN)

# Ensure data.json exists
def load_data():
    if not os.path.exists(DATA_FILE) or os.path.getsize(DATA_FILE) == 0:
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
        time.sleep(86400)  # daily check

# Telegram message handler
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if "pixeldrain.com" in text:
        add_file(text)
    else:
        await update.message.reply_text("Send a valid Pixeldrain link only!")

# Main bot
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    threading.Thread(target=check_reminders, daemon=True).start()

    app.run_polling()

if __name__ == "__main__":
    main()
