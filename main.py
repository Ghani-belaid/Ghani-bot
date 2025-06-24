import logging
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from telegram.ext import Application

from binance.client import Client
from flask import Flask, request

BOT_TOKEN = os.getenv("BOT_TOKEN")
ALLOWED_USER = os.getenv("ALLOWED_USER")  # بدون @
URL = os.getenv("WEBHOOK_URL")  # رابط موقعك من Render

# إعداد Binance
binance_client = Client()

# إعداد Flask
app = Flask(__name__)

# إعداد Telegram bot
application = Application.builder().token(BOT_TOKEN).build()

logging.basicConfig(level=logging.INFO)

# أوامر البوت
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.username != ALLOWED_USER:
        return
    await update.message.reply_text("👋 أهلاً بك في بوت Ghani لتوصيات التداول!\nاستخدم /reco")

async def reco(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.username != ALLOWED_USER:
        return
    try:
        symbol = context.args[0].upper()
        tp = float(context.args[1])
        sl = float(context.args[2])

        price = float(binance_client.get_symbol_ticker(symbol=symbol)["price"])
        tp_price = price * (1 + tp / 100)
        sl_price = price * (1 - sl / 100)

        msg = (
            f"💹 توصية لـ {symbol}:\n"
            f"🔸 السعر الحالي: {price:.2f} USDT\n"
            f"🎯 الهدف: {tp_price:.2f} USDT (+{tp}%)\n"
            f"🛑 وقف الخسارة: {sl_price:.2f} USDT (-{sl}%)"
        )
        await update.message.reply_text(msg)
    except Exception as e:
        await update.message.reply_text(f"❌ خطأ: {e}\nاكتب الأمر هكذا:\n/reco BTCUSDT 5 3")

application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("reco", reco))

# Flask route to handle Webhook
@app.route("/", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), application.bot)
    application.update_queue.put_nowait(update)
    return "ok"

# إعداد Webhook عند التشغيل
@app.before_first_request
def init():
    application.bot.delete_webhook()
    application.bot.set_webhook(url=URL)

# بدء السيرفر
if __name__ == "__main__":
    app.run(port=10000)
