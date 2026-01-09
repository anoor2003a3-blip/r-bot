import os
# هذا السطر يثبت الأدوات الناقصة تلقائياً عند تشغيل السيرفر
os.system("pip install yt-dlp python-telegram-bot")

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

def s(d):
    f = open("an.json","w")
    json.dump(d,f)
    f.close()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("أهلاً بك في بوت تحميل اليوتيوب! أرسل كلمة 'يوت' متبوعة باسم المقطع.")

async def h(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text.startswith("يوت "):
        search_query = text[4:]
        await update.message.reply_text(f"⏳ جاري تحميل '{search_query}' كملف صوتي...")
        
        try:
            # استخدام yt-dlp لتحميل الصوت
            file_name = f"audio_{random.randint(1,1000)}.mp3"
            os.system(f'yt-dlp -x --audio-format mp3 -o "{file_name}" "ytsearch:{search_query}"')
            
            if os.path.exists(file_name):
                await update.message.reply_audio(audio=open(file_name, 'rb'))
                os.remove(file_name)
            else:
                await update.message.reply_text("❌ عذراً، لم أتمكن من تحميل المقطع.")
        except Exception as e:
            await update.message.reply_text(f"❌ خطأ: تأكد من تثبيت yt-dlp في الـ Terminal")

def main():
    app = ApplicationBuilder().token(T).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), h))
    print("البوت يعمل الآن...")
    app.run_polling()

if __name__ == '__main__':
    main()
