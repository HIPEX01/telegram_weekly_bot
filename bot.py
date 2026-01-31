# bot.py
import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# ----- CONFIG -----
BOT_TOKEN = os.environ.get("BOT_TOKEN")  # Get token from Render environment

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN environment variable not set!")

# ----- LOGGING -----
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# ----- HANDLERS -----
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message with buttons when /start is used."""
    keyboard = [
        [InlineKeyboardButton("Button 1", callback_data='1')],
        [InlineKeyboardButton("Button 2", callback_data='2')],
        [InlineKeyboardButton("Button 3", callback_data='3')],
        [InlineKeyboardButton("Button 4", callback_data='4')],
        [InlineKeyboardButton("Button 5", callback_data='5')],
        [InlineKeyboardButton("Button 6", callback_data='6')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Choose a button:", reply_markup=reply_markup)

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle button presses."""
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(text=f"You pressed Button {query.data}!")

# ----- MAIN -----
def main():
    # Use ApplicationBuilder without Updater (fixes Render issues)
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Add handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_callback))

    # Run the bot
    print("Bot is running 🤖")
    app.run_polling()

if __name__ == "__main__":
    main()