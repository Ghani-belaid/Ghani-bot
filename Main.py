from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os
from binance.client import Client

# إعداد متغيرات البيئة
BOT_TOKEN = os.getenv("BOT_TOKEN")
ALLOWED_USER = os.getenv("ALLOWED_USER")

# تهيئة عميل Binance
client = Client()

# دالة حساب الهدف والستوب
def calc_price_levels(entry_price, target_pct, stop_pct):
    target = round(entry_price * (1 + target_pct/100), 2)
    stop = round(entry_price * (1 - stop_pct/100), 2)
    return target, stop

# أمر /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.username != ALLOWED_USER:
        return
    await update.message.reply_text("👋 أهلاً بك! أرسل الأمر:\n/reco BTCUSDT 5 2")

# أمر /reco
async def reco(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.username != ALLOWED_USER:
        return

    try:
        symbol = context.args[0].upper()
        target_pct = float(context.args[1])
        stop_pct = float(context.args[2])
    except:
        await update.message.reply_text("❗️الرجاء استخدام الصيغة الصحيحة:\n/reco BTCUSDT 5 2")
        return

    try:
        price = float(client.get_symbol_ticker(symbol=symbol)["price"])
    except:
        await update.message.reply_text("⚠️ لم أستطع جلب سعر العملة. تأكد من الرمز.")
        return

    target, stop = calc_price_levels(price, target_pct, stop_pct)

    msg = (
        f"🚀 توصية جديدة – {symbol}\n"
        f"📈 السعر الحالي: {price:.2f}\n"
        f"🎯 الهدف: {target:.2f}\n"
        f"🛑 الستوب: {stop:.2f}"
    )
    await update.message.reply_text(msg)

# تشغيل البوت
if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("reco", reco))
    app.run_polling()
