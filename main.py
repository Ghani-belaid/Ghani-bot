import logging
import os
import httpx
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")
ALLOWED_USER = os.getenv("ALLOWED_USER")

logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.username != ALLOWED_USER:
        return
    await update.message.reply_text("👋 أهلاً بك في بوت توصيات Ghani!\nاستخدم الأمر /reco لتوليد توصية.\nمثال:\n/reco bitcoin 5 2")

async def reco(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.username != ALLOWED_USER:
        return

    try:
        coin_id = context.args[0].lower()
        tp_percent = float(context.args[1])
        sl_percent = float(context.args[2])

        url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies=usd"
        response = httpx.get(url)
        data = response.json()

        price = float(data[coin_id]["usd"])
        tp_price = price * (1 + tp_percent / 100)
        sl_price = price * (1 - sl_percent / 100)

        message = (
            f"💹 توصية تداول لـ {coin_id.upper()}:\n"
            f"🔸 السعر الحالي: {price:.2f} USD\n"
            f"🎯 الهدف (TP): {tp_price:.2f} USD (+{tp_percent}%)\n"
            f"🛑 وقف الخسارة (SL): {sl_price:.2f} USD (-{sl_percent}%)"
        )
        await update.message.reply_text(message)

    except Exception as e:
        await update.message.reply_text(f"❌ حدث خطأ: {e}\nاستخدم الأمر بهذا الشكل:\n/reco bitcoin 5 2")

if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("reco", reco))
    app.run_polling()
