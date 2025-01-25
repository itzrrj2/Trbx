from dotenv import load_dotenv
import os
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, WebAppInfo
import logging
import asyncio
from pymongo import MongoClient
from pyrogram.enums import ChatMemberStatus
from video import download_video, upload_video  # Assuming these are custom modules
from web import keep_alive  # Assuming this is your keep-alive module

# Load environment variables from .env file
load_dotenv('config.env')  # Ensure this is the correct path to your .env file

# MongoDB Setup
mongo_url = "mongodb+srv://cphdlust:cphdlust@cphdlust.ydeyw.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(mongo_url)
db = client["cphdlust"]
users_collection = db["users"]

# Logging setup
logging.basicConfig(level=logging.INFO)

# Get the environment variables
api_id = os.getenv('TELEGRAM_API')
api_hash = os.getenv('TELEGRAM_HASH')
bot_token = os.getenv('BOT_TOKEN')
fsub_id = os.getenv('FSUB_ID')  # Channel to check if users are members
dump_chat_id = os.getenv('DUMP_CHAT_ID')  # This is where you want to send media or logs
admins_str = os.getenv('ADMINS')

# Get the ADMINS from the environment variable
if admins_str:
    admins = [int(admin.strip()) for admin in admins_str.split(',')]  # Convert to integers
    logging.info(f"Loaded Admins: {admins}")
else:
    logging.error("ADMINS variable is missing or empty.")
    admins = []  # Provide a fallback or raise an exception

# Ensure API credentials are set
if not api_id or not api_hash or not bot_token:
    raise ValueError("Missing one or more required environment variables: TELEGRAM_API, TELEGRAM_HASH, BOT_TOKEN")

# Initialize the bot
app = Client("my_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

# Command to start the bot
@app.on_message(filters.command("start"))
async def start_command(client, message):
    sticker_message = await message.reply_sticker("CAACAgIAAxkBAAEYonplzwrczhVu3I6HqPBzro3L2JU6YAACvAUAAj-VzAoTSKpoG9FPRjQE")
    await asyncio.sleep(2)
    await sticker_message.delete()
    user_mention = message.from_user.mention
    reply_message = f"ᴡᴇʟᴄᴏᴍᴇ, {user_mention}.\n\n🌟 ɪ ᴀᴍ ᴀ ᴛᴇʀᴀʙᴏx ᴅᴏᴡɴʟᴏᴀᴅᴇʀ ʙᴏᴛ."
    join_button = InlineKeyboardButton("ᴊᴏɪɴ ❤️🚀", url="https://t.me/Xstream_links2")
    developer_button = InlineKeyboardButton("ᴅᴇᴠᴇʟᴏᴘᴇʀ ⚡️", url="t.me/terABoxTer_Instagrambot")
    reply_markup = InlineKeyboardMarkup([[join_button, developer_button]])

    video_file_id = "/app/1734351426786003.mov"
    if os.path.exists(video_file_id):
        await client.send_video(chat_id=message.chat.id, video=video_file_id, caption=reply_message, reply_markup=reply_markup)
    else:
        await message.reply_text(reply_message, reply_markup=reply_markup)

# Function to check if the user is a member of the specified channel
async def is_user_member(client, user_id):
    try:
        # Check if the user is a member of the required channel
        member = await client.get_chat_member(fsub_id, user_id)
        logging.info(f"User {user_id} membership status: {member.status}")
        
        # Return True if user is either an admin, owner, or member
        if member.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER, ChatMemberStatus.MEMBER]:
            return True
        else:
            return False
    except Exception as e:
        logging.error(f"Error checking membership status for user {user_id}: {e}")
        return False

# Handle incoming text messages (For normal users and /broadcast command)
@app.on_message(filters.text)
async def handle_message(client, message: Message):
    if message.from_user is None:
        logging.error("Message does not contain user information.")
        return

    # Skip /broadcast command processing here
    if message.text.startswith("/broadcast"):
        logging.info(f"Skipping /broadcast command from {message.from_user.id}")
        return  # Do nothing if it's a broadcast command

    user_id = message.from_user.id
    user_mention = message.from_user.mention

    # Check if the user is a member of the required channel
    is_member = await is_user_member(client, user_id)

    if not is_member:
        join_button = InlineKeyboardButton("ᴊᴏɪɴ ❤️🚀", url="https://t.me/Xstream_links2")
        reply_markup = InlineKeyboardMarkup([[join_button]])
        await message.reply_text(
            "ʏᴏᴜ ᴍᴜsᴛ ᴊᴏɪɴ ᴍʏ ᴄʜᴀɴɴᴇʟ ᴛᴏ ᴜsᴇ ᴍᴇ.\nChannel 1 - https://t.me/+SwZARPAas7AwZjNl\nChannel 2 - https://t.me/+Q720C5GA9oRlNDg1\nChannel 3 - https://t.me/+QjM9OMbg4rU3ODc9",
            reply_markup=reply_markup,
        )
        return

    valid_domains = [
        'terabox.com', 'nephobox.com', '4funbox.com', 'mirrobox.com',
        'momerybox.com', 'teraboxapp.com', '1024tera.com',
        'terabox.app', 'gibibox.com', 'goaibox.com', 'terasharelink.com', 'teraboxlink.com', 'terafileshare.com'
    ]

    terabox_link = message.text.strip()

    if not any(domain in terabox_link for domain in valid_domains):
        await message.reply_text("ᴘʟᴇᴀsᴇ sᴇɴᴅ ᴀ ᴠᴀʟɪᴅ ᴛᴇʀᴀʙᴏx ʟɪɴᴋ.")
        return

    reply_msg = await message.reply_text("sᴇɴᴅɪɴɢ ʏᴏᴜ ᴛʜᴇ ᴍᴇᴅɪᴀ...🤤")
    
    try:
        file_path, thumbnail_path, video_title = await download_video(terabox_link, reply_msg, user_mention, user_id)
        await upload_video(client, file_path, thumbnail_path, video_title, reply_msg, dump_chat_id, user_mention, user_id, message)
    except Exception as e:
        logging.error(f"Error handling message: {e}")
        await handle_video_download_failure(reply_msg, terabox_link)

# Fallback for video download failure: Watch Online Option
async def handle_video_download_failure(reply_msg, url):
    """Provide a fallback option to watch the video online."""
    watch_online_button_1 = InlineKeyboardButton(
        "⚡️WATCH ONLINE 1📱", 
        web_app=WebAppInfo(url=f"https://terabox-watch.netlify.app/api2.html?url={url}")
    )
    watch_online_button_2 = InlineKeyboardButton(
        "⚡️WATCH ONLINE 2📱", 
        web_app=WebAppInfo(url=f"https://terabox-watch.netlify.app/api2.html?url={url}")
    )
    reply_markup = InlineKeyboardMarkup([
        [watch_online_button_1],
        [watch_online_button_2]
    ])
    await reply_msg.edit_text(
        "YOUR VIDEO IS READY❗️\nCLICK ON ANY OPTION BELOW TO WATCH👇👇👇",
        reply_markup=reply_markup
    )

# Broadcast command (only accessible to admins)
@app.on_message(filters.command("broadcast") & filters.user(admins))  # Only admins can use the broadcast command
async def broadcast_command(client, message):
    # Log the incoming /broadcast command
    logging.info(f"Received /broadcast command from user: {message.from_user.id}")

    # Ensure the command is a reply to a message
    if message.reply_to_message:
        logging.info(f"Message to broadcast: {message.reply_to_message.text}")  # Log the message to be broadcasted
        broadcast_msg = message.reply_to_message
        total = 0
        successful = 0
        blocked = 0
        deleted = 0
        unsuccessful = 0

        # Get all users from the MongoDB collection
        users = users_collection.find()

        pls_wait = await message.reply("<i>Broadcasting Message.. This may take some time</i>")

        for user in users:
            user_id = user["user_id"]
            try:
                await broadcast_msg.copy(user_id)
                successful += 1
            except Exception as e:
                logging.error(f"Failed to send message to {user_id}: {e}")
                unsuccessful += 1

            total += 1

        # Broadcast status
        status = f"""<b><u>Broadcast Completed</u></b>

Total Users: <code>{total}</code>
Successful: <code>{successful}</code>
Blocked Users: <code>{blocked}</code>
Deleted Accounts: <code>{deleted}</code>
Unsuccessful: <code>{unsuccessful}</code>"""

        await pls_wait.edit(status)
    else:
        msg = await message.reply("Please reply to a message to broadcast it.")
        await asyncio.sleep(8)
        await msg.delete()

if __name__ == "__main__":
    keep_alive()
    app.run()
