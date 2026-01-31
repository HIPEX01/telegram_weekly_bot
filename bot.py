# bot.py
import asyncio
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# ----- CONFIG -----
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"  # <-- Replace with your real bot token

# ----- LOGGING -----
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# ----- HANDLERS -----
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message with buttons when the command /start is issued."""
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
async def main():
    # Create the bot application
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Add handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_callback))

    # Run the bot
    print("Bot is running 🤖")
    await app.run_polling()  # This handles updates continuously

if __name__ == "__main__":
    # Start the async main function
    asyncio.run(main())