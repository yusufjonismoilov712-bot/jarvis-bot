r"""
Jarvis — Telegram bot (v3: /video reja + videoni saqlash).

Ishga tushirish (PowerShell):
  cd C:\Users\Hp\Downloads
  $env:BOT_TOKEN="BOTFATHER_TOKEN"
  py -3.13 jarvis_bot_v3.py

Videolar saqlanadi: Downloads\jarvis_videos
Eslatma: Telegram bot orqali 20 MB gacha fayl qabul qiladi.
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
VIDEO_DIR = os.path.join(os.path.expanduser("~"), "Downloads", "jarvis_videos")
os.makedirs(VIDEO_DIR, exist_ok=True)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Salom, men Jarvis. Buyruqlar:\n"
        "/start - yordam\n"
        "/vaqt - hozirgi vaqt\n"
        "/salom - salomlashish\n"
        "/video <mavzu> - video reja tayyorlash\n\n"
        "Videoni shu yerga yuborsangiz, men uni kompyuterga saqlayman."
    )


async def vaqt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    now = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    await update.message.reply_text(f"Hozirgi vaqt: {now}")


async def salom(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name = update.effective_user.first_name or "do'st"
    await update.message.reply_text(f"Salom, {name}! Qanday yordam bera olaman?")


async def video_reja(update: Update, context: ContextTypes.DEFAULT_TYPE):
    topic = " ".join(context.args).strip()
    if not topic:
        await update.message.reply_text("Mavzuni yozing. Misol: /video kunlik intizom")
        return

    tag = topic.replace(" ", "")
    outline = (
        f"Video reja: {topic}\n\n"
        "1) HOOK (0-3 soniya)\n"
        f"Matn: \"{topic} haqida hech kim sizga aytmagan narsa.\"\n\n"
        "2) SAHNALAR (har biri 3 soniya)\n"
        "Sahna 1: muammo ko'rsatiladi\n"
        "Sahna 2: sababi tushuntiriladi\n"
        "Sahna 3: yechim va birinchi qadam\n\n"
        "3) SARLAVHA VARIANTLARI\n"
        f"- {topic.title()}: 3 ta oddiy qadam\n"
        f"- Nega {topic.lower()} ishlamayapti?\n"
        f"- {topic.title()} uchun 7 kunlik reja\n\n"
        "4) TAVSIF\n"
        f"Bu videoda {topic.lower()} haqida amaliy maslahatlar beriladi. "
        "Obuna bo'ling va o'z tajribangizni izohda yozing.\n\n"
        "5) TEGLAR\n"
        f"#{tag} #motivatsiya #intizom #shorts"
    )
    await update.message.reply_text(outline)


async def save_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message
    media = msg.video or msg.document
    if media is None:
        return

    try:
        tg_file = await media.get_file()
    except Exception as exc:
        logging.exception("Faylni olishda xato")
        await msg.reply_text(
            f"Faylni olib bo'lmadi: {exc}\n"
            "Telegram bot orqali 20 MB dan katta fayl qabul qilmaydi."
        )
        return

    original = getattr(media, "file_name", None)
    stamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    name = original or f"video_{stamp}.mp4"
    path = os.path.join(VIDEO_DIR, f"{stamp}_{name}")

    await tg_file.download_to_drive(path)
    await msg.reply_text(f"Video saqlandi:\n{path}")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()
    if "salom" in text:
        await update.message.reply_text("Salom! Nima kerak?")
    elif "rahmat" in text:
        await update.message.reply_text("Arzimaydi.")
    else:
        await update.message.reply_text("Tushunmadim. /start yozib buyruqlarni ko'ring.")


def main():
    if BOT_TOKEN == "BU_YERGA_TOKEN_YOZING":
        raise SystemExit('BOT_TOKEN ni kiriting: $env:BOT_TOKEN="..."')

    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("vaqt", vaqt))
    app.add_handler(CommandHandler("salom", salom))
    app.add_handler(CommandHandler("video", video_reja))
    app.add_handler(MessageHandler(filters.VIDEO | filters.Document.VIDEO, save_video))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    print(f"Jarvis ishga tushdi. Videolar: {VIDEO_DIR}")
    print("To'xtatish uchun Ctrl+C.")
    app.run_polling()


if __name__ == "__main__":
    main()
