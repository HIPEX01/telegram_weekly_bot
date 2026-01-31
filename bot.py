# bot.py
import asyncio
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
from apscheduler.schedulers.background import BackgroundScheduler
from config import BOT_TOKEN, CHAT_ID, ADMIN_ID

# ---------------- BUTTONS ----------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📖 Show weekly message", callback_data="show")],
        [InlineKeyboardButton("ℹ️ Help", callback_data="help")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Hi 👋\nTap a button:", reply_markup=reply_markup)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "show":
        await query.edit_message_text("Here is your weekly message! ✅")
    elif query.data == "help":
        await query.edit_message_text("Use the buttons to interact with the bot.")

# ---------------- WEEKLY MESSAGE ----------------
async def send_weekly_message(app):
    try:
        await app.bot.send_message(chat_id=CHAT_ID, text="Weekly message sent! 📅")
    except Exception as e:
        print("Error sending weekly message:", e)

def start_scheduler(app):
    scheduler = BackgroundScheduler()
    scheduler.add_job(lambda: app.create_task(send_weekly_message(app)),
                      trigger="cron", day_of_week="mon", hour=12, minute=0)
    scheduler.start()

# ---------------- ADMIN COMMAND ----------------
async def set_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("❌ You are not allowed!")
        return
    new_text = " ".join(context.args)
    if not new_text:
        await update.message.reply_text("Usage: /set Your new weekly message")
        return
    global WEEKLY_MESSAGE
    WEEKLY_MESSAGE = new_text
    await update.message.reply_text(f"✅ Weekly message updated:\n{WEEKLY_MESSAGE}")

# ---------------- MAIN ----------------
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(CommandHandler("set", set_message))

    start_scheduler(app)

    print("Bot is running 🤖")
    app.run_polling(close_loop=False)

if __name__ == "__main__":
    WEEKLY_MESSAGE = "This is the default weekly message! 📅"
    main()