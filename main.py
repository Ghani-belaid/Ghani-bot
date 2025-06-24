import logging
import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")
ALLOWED_USER = os.getenv("ALLOWED_USER")

logging.basicConfig(level=logging.INFO)

COINGECKO_URL = "https://api.coingecko.com/api/v3/simple/price"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.username != ALLOWED_USER:
        return
    await update.message.reply_text(
        "👋 أهلاً بك في بوت توصيات Ghani!\nاستخدم الأمر /reco لتوليد توصية.\nمثال:\n/reco bitcoin 5 2"
    )

async def reco(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.username != ALLOWED_USER:
        return

    try:
        symbol = context.args[0].lower()
        tp_percent = float(context.args[1])
        sl_percent = float(context.args[2])

        response = requests.get(f"{COINGECKO_URL}?ids={symbol}&vs_currencies=usd")
        data = response.json()

        if symbol not in data:
            await update.message.reply_text("❌ العملة غير موجودة أو غير مدعومة من CoinGecko.")
            return

        price = float(data[symbol]['usd'])

        tp_price = price * (1 + tp_percent / 100)
        sl_price = price * (1 - sl_percent / 100)

        message = (
            f"💹 توصية تداول لـ {symbol}:\n"
            f"🔸 السعر الحالي: {price:.2f} USDT\n"
            f"🎯 الهدف (TP): {tp_price:.2f} USDT (+{tp_percent}%)\n"
            f"🛑 وقف الخسارة (SL): {sl_price:.2f} USDT (-{sl_percent}%)"
        )
        await update.message.reply_text(message)

    except Exception as e:
        await update.message.reply_text(f"❌ خطأ: {e}\nاستخدم الأمر بهذا الشكل:\n/reco bitcoin 5 2")

if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("reco", reco))
    app.run_polling()
