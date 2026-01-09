import os
import json
import random
import asyncio
from telegram import *
from telegram.ext import *

# الإعدادات
T = "8303634172:AAFAu8zC7RWFPRSOOXM_lYAflVKt489stKw"
D = 8217288002

def g():
    try:
        f = open("an.json","r")
        d = json.load(f)
        f.close()
        return d
    except:
        return []

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("أهلاً بك! البوت عاد للعمل.")

async def h(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text.startswith("يوت "):
        await update.message.reply_text("عذراً، ميزة التحميل متوقفة حالياً للصيانة.")

def main():
    app = ApplicationBuilder().token(T).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), h))
    print("البوت يعمل الآن...")
    app.run_polling()

if __name__ == '__main__':
    main()
