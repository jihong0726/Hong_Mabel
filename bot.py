import json, os, re
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, ContextTypes,
    CommandHandler, MessageHandler, CallbackQueryHandler, filters
)

BOT_TOKEN = os.getenv("8573997245:AAEBaTctsWgygNdMaIfY8qbw-RNk8QaY8EQ", "")
OWNER_ID = int(os.getenv("Kong_Ji_Hong", "0"))
DATA_FILE = "data.json"

USER_STATE = {}

REGIONS = [
    "Kuala Lumpur", "Selangor", "Penang", "Johor",
    "Melaka", "Perak", "Pahang", "Sabah", "Sarawak", "其他"
]
FOOD_TYPES = ["面", "饭", "甜点", "饮料", "西餐", "中餐", "其他"]

def load_data():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def clean_url(url: str) -> str:
    url = url.strip()
    # 取出文本里第一个URL（如果用户粘贴一段话）
    m = re.search(r"(https?://\S+)", url)
    url = m.group(1) if m else url
    return url.split("?")[0]

def guess_name(url: str) -> str:
    m = re.search(r"instagram\.com/([^/?#]+)", url)
    if m: return m.group(1)
    m = re.search(r"tiktok\.com/@([^/?#]+)", url)
    if m: return m.group(1)
    return url

def is_owner(update: Update) -> bool:
    uid = update.effective_user.id if update.effective_user else 0
    return OWNER_ID == 0 or uid == OWNER_ID

async def guard(update: Update):
    if not is_owner(update):
        # 只你能用：其他人一律不响应或给一句话
        if update.message:
            await update.message.reply_text("这个 bot 是私用的～")
       
