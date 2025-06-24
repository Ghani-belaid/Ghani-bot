import logging
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from binance.client import Client

BOT_TOKEN = os.getenv("BOT_TOKEN")
ALLOWED_USER = os.getenv("ALLOWED_USER")

logging.basicConfig(level=logging.INFO)

binance_client = Client()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.username != ALLOWED_USER:
        return
    await update.message.reply_text("👋 مرحبًا بك في بوت توصيات Ghani! \nاكتب /reco BTCUSDT 5 2")

async def reco(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.username != ALLOWED_USER:
        return

    try:
        symbol = context.args[0].upper()
        tp_percent = float(context.args[1])
        sl_percent = float(context.args[2])

        ticker = binance_client.get_symbol_ticker(symbol=symbol)
        price = float(ticker['price'])

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
        await update.message.reply_text(f"❌ خطأ: {e}\nاكتب الأمر بهذا الشكل:\n/reco BTCUSDT 5 2")

if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("reco", reco))
    app.run_polling()
