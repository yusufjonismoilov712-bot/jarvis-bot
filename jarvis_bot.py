"""
Jarvis — oddiy Telegram bot.

Ishga tushirish:
1. pip install python-telegram-bot==21.6
2. BOT_TOKEN ni @BotFather dan olib, quyiga qo'ying (yoki muhit o'zgaruvchisi sifatida).
3. python jarvis_bot.py
"""

import os
import datetime
import logging

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

BOT_TOKEN = os.getenv("BOT_TOKEN", "BU_YERGA_TOKEN_YOZING")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Salom, men Jarvis. Buyruqlar:\n"
        "/start - yordam\n"
        "/vaqt - hozirgi vaqt\n"
        "/salom - salomlashish\n\n"
        "Yoki shunchaki yozing, men javob beraman."
    )


async def vaqt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    now = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    await update.message.reply_text(f"Hozirgi vaqt: {now}")


async def salom(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name = update.effective_user.first_name or "do'st"
    await update.message.reply_text(f"Salom, {name}! Qanday yordam bera olaman?")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()
    if "salom" in text:
        await update.message.reply_text("Salom! Nima kerak?")
    elif "rahmat" in text:
        await update.message.reply_text("Arzimaydi.")
    else:
        await update.message.reply_text(
            "Tushunmadim. /start yozib buyruqlarni ko'ring."
        )


def main():
    if BOT_TOKEN == "BU_YERGA_TOKEN_YOZING":
        raise SystemExit("BOT_TOKEN ni kiriting.")

    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("vaqt", vaqt))
    app.add_handler(CommandHandler("salom", salom))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    print("Jarvis ishga tushdi. To'xtatish uchun Ctrl+C.")
    app.run_polling()


if __name__ == "__main__":
    main()
