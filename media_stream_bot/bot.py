import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

from config import BOT_TOKEN

BASE_URL = "https://your-koyeb-url.koyeb.app"  # Change this later after deploying
SAVE_PATH = "files"
os.makedirs(SAVE_PATH, exist_ok=True)

async def handle_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.document and not update.message.video:
        return

    file_obj = update.message.document or update.message.video
    file_id = file_obj.file_id
    file_name = file_obj.file_name or f"{file_id}.mp4"
    file_path = os.path.join(SAVE_PATH, file_name)

    file = await context.bot.get_file(file_id)
    await file.download_to_drive(file_path)

    stream_link = f"{BASE_URL}/stream/{file_name}"
    download_link = f"{BASE_URL}/download/{file_name}"

    keyboard = [
        [InlineKeyboardButton("▶ Stream", url=stream_link)],
        [InlineKeyboardButton("⬇ Download", url=download_link)],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text("File saved successfully!", reply_markup=reply_markup)

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.Document.ALL | filters.Video.ALL, handle_file))
    app.run_polling()
