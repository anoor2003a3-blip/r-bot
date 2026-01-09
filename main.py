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
        return {"r":{},"t":{},"s":{},"m":""}

def s(d):
    f = open("an.json","w")
    json.dump(d,f)
    f.close()

async def inf(u,c,i,db,w):
    try:
        t = await c.bot.get_chat(i)
        n = t.first_name
        un = f"@{t.username}" if t.username else "لا يوجد"
        v = db["s"].get(str(i),0)
        m = f"👤: {n}\n🆔: {i}\n🔗: {un}\n💬: {v}\n📌: {w}"
        try:
            p = await c.bot.get_user_profile_photos(i,limit=1)
            if p.total_count > 0:
                await u.message.reply_photo(p.photos[0][-1].file_id,caption=m)
            else: await u.message.reply_text(m)
        except: await u.message.reply_text(m)
    except: await u.message.reply_text("❌")

async def h(u,c):
    if not u.message or not u.message.text: return
    db = g()
    tx = u.message.text
    id = str(u.effective_user.id)
    db["s"][id] = db["s"].get(id,0) + 1
    s(db)

    # ميزة يوت (تحميل صوت)
    if tx.startswith("يوت"):
        nm = tx.replace("يوت","").strip()
        if nm:
            await u.message.reply_text(f"⏳ جاري تحميل '{nm}' كملف صوتي...")
            try:
                # هذا الجزء يحتاج yt-dlp مثبت في الجهاز
                import yt_dlp
                opts = {'format':'bestaudio','outtmpl':'s.mp3','quiet':True}
                with yt_dlp.YoutubeDL(opts) as y:
                    y.download([f"ytsearch1:{nm}"])
                await u.message.reply_audio(audio=open('s.mp3','rb'), title=nm)
                os.remove('s.mp3')
            except Exception as e:
                await u.message.reply_text(f"❌ خطأ: تأكد من تثبيت yt-dlp في الـ Terminal")
            return

    if tx == "ا":
        t = u.message.reply_to_message.from_user if u.message.reply_to_message else u.effective_user
        await inf(u,c,t.id,db,"كشف")
        return

    if tx == "لو خيروك":
        ls = ["تاكل بصل أو تشرب خل؟", "تنام بقبر أو تعيش بغابة؟"]
        await u.message.reply_text(random.choice(ls))
        return

    if tx in ["اسالني", "اسألني"]:
        ls = ["شنو برجك؟", "شنو حلمك؟"]
        await u.message.reply_text(random.choice(ls))
        return

    if tx.startswith("همسه") or tx.startswith("همسة"):
        if u.message.reply_to_message:
            tg = u.message.reply_to_message.from_user
            ms = tx.replace("همسة","").replace("همسه","").strip()
            k = f"h_{tg.id}_{id}_{random.randint(1,99)}"
            c.bot_data.setdefault('w',{})[k] = ms
            await c.bot.send_message(D, f"👤 همسة من {id}: {ms}")
            from telegram import InlineKeyboardButton as B, InlineKeyboardMarkup as M
            await u.message.reply_text("🔒 تم القفل",reply_markup=M([[B(f"📩 {tg.first_name}",callback_data=k)]]))
            return

    if tx == "البوت" and int(id) == D:
        from telegram import InlineKeyboardButton as B, InlineKeyboardMarkup as M
        btns = [[B("+ر",callback_data="ar"),B("-ر",callback_data="dr")],[B("+ت",callback_data="at"),B("-ت",callback_data="dt")]]
        await u.message.reply_text("⚙️ لوحة التحكم:",reply_markup=M(btns))
        return

    m = db.get("m","")
    if ":" in tx and m:
        k,v = tx.split(":",1)
        if "ar" in m: db["r"][k.strip()] = v.strip()
        if "at" in m: db["t"][k.strip()] = v.strip()
        db["m"] = ""; s(db); await u.message.reply_text("✅"); return

    if tx in db["t"]: await inf(u,c,db["t"][tx],db,tx); return
    if tx in db["r"]: await u.message.reply_text(db["r"][tx])

async def cl(u,c):
    q = u.callback_query
    db, id = g(), str(q.from_user.id)
    if q.data in ["ar","dr","at","dt"]:
        db["m"] = f"{q.data}_{id}"; s(db)
        await q.message.reply_text("ارسل (الكلمة:الرد)")
    elif q.data.startswith("h_"):
        p = q.data.split("_")
        if id in [p[1],p[2],str(D)]:
            v = c.bot_data.get('w',{}).get(q.data,"!")
            await q.answer(v,show_alert=True)
        else: await q.answer("❌ ليست لك", show_alert=True)

app = Application.builder().token(T).build()
app.add_handler(MessageHandler(filters.TEXT,h))
app.add_handler(CallbackQueryHandler(cl))
print("🚀 STARTED V116")
app.run_polling()
