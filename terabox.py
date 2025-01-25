import re 
import logging
import asyncio
import os
from pymongo import MongoClient
from dotenv import load_dotenv
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from pyrogram.errors import FloodWait, UserIsBlocked, InputUserDeactivated
from status import format_progress_bar  # Assuming this is a custom module
from video import download_video, upload_video  # Assuming these are custom modules
from database.database import present_user, add_user, full_userbase, del_user  # Assuming these are custom modules
from web import keep_alive
from config import *

load_dotenv('config.env', override=True)

logging.basicConfig(level=logging.INFO)

ADMINS = list(map(int, os.environ.get('ADMINS', '7064434873').split()))
api_id = os.environ.get('TELEGRAM_API', '')
api_hash = os.environ.get('TELEGRAM_HASH', '')
bot_token = os.environ.get('BOT_TOKEN', '')
dump_id = int(os.environ.get('DUMP_CHAT_ID', ''))
fsub_id = int(os.environ.get('FSUB_ID', ''))

mongo_url = os.environ.get('MONGO_URL', 'mongodb+srv://cphdlust:cphdlust@cphdlust.ydeyw.mongodb.net/?retryWrites=true&w=majority')
client = MongoClient(mongo_url)
db = client['cphdlust']
users_collection = db['users']

def extract_links(text):
    url_pattern = r'(https?://[^\s]+)'  # Regex to capture http/https URLs
    return re.findall(url_pattern, text)

app = Client("my_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

@app.on_message(filters.command("start"))
async def start_command(client, message):
    user_id = message.from_user.id
    user_mention = message.from_user.mention

    if not await present_user(user_id):
        try:
            await add_user(user_id)
            logging.info(f"Added user {user_id} to the database")
        except Exception as e:
            logging.error(f"Failed to add user {user_id} to the database: {e}")

    reply_message = (
        f"🌟 Welcome to the Ultimate TeraBox Downloader Bot, {user_mention}!\n\n"
        "🚀 **Why Choose This Bot?**\n"
        "- **Unmatched Speed**: Experience the fastest and most powerful TeraBox downloader on Telegram. ⚡\n"
        "- **100% Free Forever**: No hidden fees or subscriptions—completely free for everyone! 🆓\n"
        "- **Seamless Downloads**: Easily download TeraBox files and have them sent directly to you. 🎥📁\n"
        "- **24/7 Availability**: Access the bot anytime, anywhere, without downtime. ⏰\n\n"
        "🎯 **How It Works**\n"
        "Simply send a TeraBox link, and let the bot handle the rest. It's quick, easy, and reliable! 🚀\n\n"
        "💎 **Your Ultimate Telegram Tool**—crafted to make your experience effortless and enjoyable.\n\n"
        "Join our growing community to discover more features and stay updated! 👇"
    )
    join_button = InlineKeyboardButton("Join ❤️🚀", url="https://t.me/Xstream_links2")
    developer_button = InlineKeyboardButton("Developer ⚡️", url="https://t.me/Xstream_Links2")
    reply_markup = InlineKeyboardMarkup([[join_button, developer_button]])
    await message.reply_text(reply_message, reply_markup=reply_markup)

@app.on_message(filters.text)
async def handle_message(client, message: Message):
    user_id = message.from_user.id
    if not await present_user(user_id):
        try:
            await add_user(user_id)
        except Exception as e:
            logging.error(f"Failed to add user {user_id} to the database: {e}")

    links = extract_links(message.text)
    if not links:
        await message.reply_text("Please send a valid link.")
        return

    for terabox_link in links:
        if not "terabox" in terabox_link.lower():
            await message.reply_text(f"{terabox_link} is not a valid Terabox link.")
            continue
            
        reply_msg = await message.reply_text("🔄 Retrieving your TeraBox video. Please wait...")

        try:
            file_path, thumbnail_path, video_title = await download_video(terabox_link, reply_msg, message.from_user.mention, user_id)
            await upload_video(client, file_path, thumbnail_path, video_title, reply_msg, dump_id, message.from_user.mention, user_id, message)
        except Exception as e:
            logging.error(f"Error handling message: {e}")
            await handle_video_download_failure(reply_msg, terabox_link)

async def handle_video_download_failure(reply_msg, url):
    """Handle cases when video download fails by showing a 'Watch Online' option."""
    watch_online_button_1 = InlineKeyboardButton(
        "📺 CLICK TO WATCH (Option 1)", 
        web_app=WebAppInfo(url=f"https://terabox-watch.netlify.app/api2.html?url={url}")
    )
    watch_online_button_2 = InlineKeyboardButton(
        "📺 CLICK TO WATCH (Option 2)", 
        web_app=WebAppInfo(url=f"https://terabox-watch.netlify.app/?url={url}")
    )
    reply_markup = InlineKeyboardMarkup([
        [watch_online_button_1],
        [watch_online_button_2]
    ])
    await reply_msg.edit_text(
        "❌ Unable to download your video. You can watch it online using the options below:",
        reply_markup=reply_markup
    )

if __name__ == "__main__":
    keep_alive()
    app.run()
