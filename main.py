from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from datetime import datetime
import json
import os
import time
import asyncio
import traceback
import telegram
import base64
import ast

# === BOT TOKEN DAN ADMIN ===
TOKEN = "7256145248:AAGQSNOjkK-G-dLfL-zYj5ohydGP-SytZvQ"
ADMIN_IDS = [7256145248, 6360597652]

# === DATA TERENKRIPSI ===
_encoded_fresh_devices = "eyJTQU1TVU5HIjogIksiLCAiVklWTyI6ICJCIiwgIklORklOSVgiOiAiSyIsICJPUFBPIjogIksiLCAiUkVETk9UIjogIkIiLCAiUkVBTE1FIjogIksiLCAiUk9HIjogIksiLCAiVEVETk8iOiAiQiIsICJQT0NPIjogIkIiLCAiSVAgWFIiOiAiQiIsICJJUCA3LTE1IjogIkIifQ=="
FRESH_DEVICES = ast.literal_eval(base64.b64decode(_encoded_fresh_devices).decode())

premium_users = {}

# === PREMIUM ===
def save_premium():
    with open("premium.json", "w") as f:
        json.dump({str(k): v.isoformat() if v else None for k, v in premium_users.items()}, f)

def load_premium():
    if not os.path.exists("premium.json"):
        for admin_id in ADMIN_IDS:
            premium_users[admin_id] = None
        save_premium()
        return

    try:
        with open("premium.json", "r") as f:
            data = json.load(f)
            for uid, exp in data.items():
                premium_users[int(uid)] = datetime.fromisoformat(exp) if exp else None
    except Exception as e:
        print(f"Gagal load premium.json: {e}")
        for admin_id in ADMIN_IDS:
            premium_users[admin_id] = None
        save_premium()

load_premium()

def is_admin(user_id):
    return user_id in ADMIN_IDS

def is_premium(user_id):
    if user_id in premium_users:
        exp = premium_users[user_id]
        return exp is None or exp > datetime.now()
    return False

# === RUMUS TERENKRIPSI ===
def rumus_3_match(m1):
    m1 = int(m1)
    encoded = "eyIxOSI6ICJLRUNJTCIsICIyMSI6ICJLRUNJTCIsICIyMyI6ICJCRVNBUiIsICIyNCI6ICJCRVNBUiIsICIyNSI6ICJLRUNJTCIsICIyNiI6ICJLRUNJTCIsICIyNyI6ICJLRUNJTCIsICIyOCI6ICJCRVNBUiIsICIyOSI6ICJCRVNBUiIsICIzMCI6ICJLRUNJTCIsICIzMiI6ICJCRVNBUiIsICIzMyI6ICJLRUNJTCIsICIzNCI6ICJCRVNBUiIsICIzNSI6ICJCRVNBUiIsICIzNiI6ICJLRUNJTCIsICIzNyI6ICJCRVNBUiIsICIzOSI6ICJCRVNBUiIsICI0MCI6ICJCRVNBUiIsICI0MSI6ICJLRUNJTCIsICI0MiI6ICJCRVNBUiIsICI0MyI6ICJCRVNBUiIsICI0NCI6ICJCRVNBUiIsICI0NSI6ICJLRUNJTCJ9"
    rules = ast.literal_eval(base64.b64decode(encoded).decode())
    return rules.get(str(m1), None), "Fix Rule" if str(m1) in rules else (None, None)

def rumus_1dadu(m1):
    m1 = int(m1)
    encoded = "eyIxIjogIktFQ0lMIiwgIjIiOiAiQkVTQVIiLCAiMyI6ICJLRUNJTCIsICI0IjogIktFQ0lMIiwgIjUiOiAiQkVTQVIiLCAiNiI6ICJLRUNJTCJ9"
    rules = ast.literal_eval(base64.b64decode(encoded).decode())
    return rules.get(str(m1), "KECIL" if m1 <= 3 else "BESAR"), "Fix Rule"

def rumus_1match9dadu(m1):
    m1 = int(m1)
    encoded = "eyIxNyI6ICJLRUNJTCIsICIxOCI6ICJCRVNBUiIsICIyMCI6ICJCRVNBUiIsICIyMSI6ICJLRUNJTCIsICIyMiI6ICJCRVNBUiIsICIyMyI6ICJCRVNBUiIsICIyNCI6ICJCRVNBUiIsICIyNSI6ICJLRUNJTCIsICIyNiI6ICJLRUNJTCIsICIyNyI6ICJLRUNJTCIsICIyOCI6ICJCRVNBUiIsICIyOSI6ICJCRVNBUiIsICIzMCI6ICJLRUNJTCIsICIzMSI6ICJLRUNJTCIsICIzMiI6ICJLRUNJTCIsICIzMyI6ICJLRUNJTCIsICIzNCI6ICJCRVNBUiIsICIzNSI6ICJCRVNBUiIsICIzNiI6ICJCRVNBUiIsICIzNyI6ICJCRVNBUiIsICIzOCI6ICJCRVNBUiIsICIzOSI6ICJCRVNBUiIsICI0MCI6ICJCRVNBUiIsICI0MSI6ICJCRVNBUiIsICI0MiI6ICJLRUNJTCJ9"
    rules = ast.literal_eval(base64.b64decode(encoded).decode())
    return rules.get(str(m1), None), "Fix Rule" if str(m1) in rules else (None, None)

# === MENU ===
menu_keyboard = [
    ["Fresh Device"],
    ["PRED  9 DADU 3 MATCH 🔥"],
    ["PRED  1 DADU 1 MATCH 🔥"],
    ["PRED  9 DADU 1 MATCH 🔥"]
]
menu_markup = ReplyKeyboardMarkup(menu_keyboard, resize_keyboard=True)

# === HANDLERS ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.chat.type not in ["private", "group", "supergroup"]:
        return
    if not is_premium(update.effective_user.id):
        return
    await update.message.reply_text("Pilih Menu:", reply_markup=menu_markup)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or update.message.chat.type not in ["private", "group", "supergroup"]:
        return

    user_id = update.effective_user.id
    if not is_premium(user_id):
        return

    text = update.message.text

    if text == "Fresh Device":
        result = "\n".join([f"{k} ➤ {v}" for k, v in FRESH_DEVICES.items()])
        await update.message.reply_text(f"📱 *Fresh Devices:*\n\n{result}", parse_mode="Markdown")
    elif text in ["PRED  9 DADU 3 MATCH 🔥", "PRED  1 DADU 1 MATCH 🔥", "PRED  9 DADU 1 MATCH 🔥"]:
        await update.message.reply_text("🤖 ISI ANGKA DADU LAST GAME")
        context.user_data['mode'] = text
    elif 'mode' in context.user_data:
        if not text.isdigit():
            await update.message.reply_text("❗ Masukkan angka yang valid (hanya angka).")
            return
        try:
            angka = int(text)
            mode = context.user_data.pop('mode')
            if "3 MATCH" in mode:
                hasil, _ = rumus_3_match(angka)
                if hasil is None:
                    await update.message.reply_text("❌ ANGKA TIDAK COCOK")
                    return
            elif "1 DADU 1 MATCH" in mode:
                hasil, _ = rumus_1dadu(angka)
            elif "9 DADU 1 MATCH" in mode:
                hasil, _ = rumus_1match9dadu(angka)
                if hasil is None:
                    await update.message.reply_text("❌ ANGKA TIDAK COCOK")
                    return
            else:
                hasil = "-"

            await update.message.reply_text(f"""
🎯 RAMALAN AI HARI INI
━━━━━━━━━━━━━━━
🧩 Nomor Pilihan: {angka}
✨ Prediksi: {hasil}
""")
        except:
            await update.message.reply_text("❗ Masukkan angka yang valid.")

# === PREMIUM TOOLS ===
async def add_premium(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ADMIN_IDS:
        return
    if not update.message.reply_to_message:
        await update.message.reply_text("❌ Reply pesan user yang ingin di-premium-kan.")
        return
    target = update.message.reply_to_message.from_user
    premium_users[target.id] = None
    save_premium()
    await update.message.reply_text(f"✅ {target.mention_html()} sekarang Premium (permanen).", parse_mode="HTML")

async def del_premium(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ADMIN_IDS:
        return
    if not update.message.reply_to_message:
        await update.message.reply_text("❌ Reply pesan user yang ingin dihapus dari premium.")
        return
    target = update.message.reply_to_message.from_user
    if target.id in premium_users:
        del premium_users[target.id]
        save_premium()
        await update.message.reply_text(f"✅ {target.mention_html()} sudah dihapus dari Premium.", parse_mode="HTML")
    else:
        await update.message.reply_text("❗ User tersebut tidak ada di daftar premium.")

# === SAFE POLLING ===
start_time = time.time()

async def safe_polling(app):
    while True:
        try:
            await app.run_polling()
        except telegram.error.RetryAfter as e:
            print(f"[⚠️ Flood Control] Ditunda {e.retry_after} detik...")
            await asyncio.sleep(e.retry_after)
        except Exception as e:
            print("❌ Error saat polling:")
            traceback.print_exc()
            await asyncio.sleep(5)

# === MAIN ===
if __name__ == '__main__':
    import nest_asyncio
    nest_asyncio.apply()

    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("addpremium", add_premium))
    app.add_handler(CommandHandler("delpremium", del_premium))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🤖 Bot is running...")

    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(safe_polling(app))
    except (KeyboardInterrupt, SystemExit):
        print("\n🛑 Bot stopped.")
    finally:
        uptime = time.time() - start_time
        jam = int(uptime // 3600)
        menit = int((uptime % 3600) // 60)
        print(f"🕐 Durasi aktif: {jam} jam {menit} menit.")