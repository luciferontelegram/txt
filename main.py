# Don't Remove Credit Tg - @Ydvdevil4
# Ask Doubt on telegram @Ydvdevil4

import os
import re
import sys
import json
import time
import aiohttp
import asyncio
import requests
import subprocess
import urllib.parse
import cloudscraper
import datetime
import random
import ffmpeg
import logging 
import yt_dlp
from aiohttp import web
from core import *
from urllib.parse import urlparse, parse_qs
from bs4 import BeautifulSoup
from yt_dlp import YoutubeDL
import yt_dlp as youtube_dl
import cloudscraper
import m3u8
import core as helper
from utils import progress_bar
from vars import API_ID, API_HASH, BOT_TOKEN
from aiohttp import ClientSession
from pyromod import listen
from subprocess import getstatusoutput
from pytube import YouTube
from pymongo import MongoClient
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.errors import FloodWait
from pyrogram.errors.exceptions.bad_request_400 import StickerEmojiInvalid
from pyrogram.types.messages_and_media import message
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Temporary in-memory storage for premium users
PREMIUM_USERS = set()  # Store premium user IDs
OWNER_ID = 7410986089  # Replace with the actual owner's user ID
SUDO_USERS = [7410986089, 6911302498]  # List of sudo users

try:
    logger.info("Initializing Telegram bot...")
    bot = Client(
        "bot",
        api_id=int(API_ID),
        api_hash=API_HASH,
        bot_token=BOT_TOKEN
    )
    logger.info("Bot initialization successful")
except Exception as e:
    logger.error(f"Bot initialization failed: {str(e)}")
    sys.exit(1)

# Simplified premium system functions
def is_premium_user(user_id: int) -> bool:
    """Check if user is premium"""
    return user_id in PREMIUM_USERS

async def add_premium_user(user_id: int, days: int):
    """Add premium user"""
    PREMIUM_USERS.add(user_id)

async def remove_premium_user(user_id: int):
    """Remove premium user"""
    PREMIUM_USERS.discard(user_id)

async def get_premium_users():
    """Get all premium users"""
    return list(PREMIUM_USERS)

# Function to check if a user is authorized
def is_authorized(user_id: int) -> bool:
    return (user_id == OWNER_ID or 
            user_id in SUDO_USERS or 
            user_id == AUTH_CHANNEL or 
            is_premium_user(user_id))

# Log channel configuration
LOG_CHANNEL = int(os.environ.get("LOG_CHANNEL", "-1002339598092"))

cookies_file_path = os.getenv("COOKIES_FILE_PATH", "youtube_cookies.txt")

# Image URLs
cpimg = "https://graph.org/file/5ed50675df0faf833efef-e102210eb72c1d5a17.jpg"  

async def show_random_emojis(message):
    emojis = ['🎊', '🔮', '😎', '⚡️', '🚀', '✨', '💥', '🎉', '🥂', '🍾', '🦠', '🤖', '❤️‍🔥', '🕊️', '💃', '🥳','🐅','🦁']
    emoji_message = await message.reply_text(' '.join(random.choices(emojis, k=1)))
    return emoji_message
    
# Auth channel
AUTH_CHANNEL = -1002339598092

# Inline keyboard for start command
keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("🇮🇳ʙᴏᴛ ᴍᴀᴅᴇ ʙʏ🇮🇳", url=f"https://t.me/Ydvdevil4") ],
                    [
                    InlineKeyboardButton("🔔ᴜᴘᴅᴀᴛᴇ ᴄʜᴀɴɴᴇʟ🔔", url="https://t.me/Ydvdevil4") ],
                    [
                    InlineKeyboardButton("🦋ғᴏʟʟᴏᴡ ᴜs🦋", url="https://t.me/Ydvdevil4")                              
                ],           
            ]
      )
    
# Image URLs for the random image feature
image_urls = [
    "https://graph.org/file/5ed50675df0faf833efef.jpg",
    "https://graph.org/file/996d4fc24564509244988.jpg",
    "https://graph.org/file/6593f76ddd8c735ae3ce2.jpg"
]
random_image_url = random.choice(image_urls)

# Caption for the image
caption = (
        "**ʜᴇʟʟᴏ👋**\n\n"
        "➠ **ɪ ᴀᴍ ᴛxᴛ ᴛᴏ ᴠɪᴅᴇᴏ ᴜᴘʟᴏᴀᴅᴇʀ ʙᴏᴛ.**\n"
        "➠ **ғᴏʀ ᴜsᴇ ᴍᴇ sᴇɴᴅ /Devil.\n"
        "➠ **ғᴏʀ ɢᴜɪᴅᴇ sᴇɴᴅ /help."
)
    
# Start command handler
@bot.on_message(filters.command(["start"]))
async def start_command(bot: Client, message: Message):
    await bot.send_photo(chat_id=message.chat.id, photo=random_image_url, caption=caption, reply_markup=keyboard)
    
# Stop command handler
@bot.on_message(filters.command("stop"))
async def restart_handler(_, m: Message):
    if not is_authorized(m.from_user.id):
        await m.reply_text("**🚫 You are not authorized to use this command.**")
        return
        
    await m.reply_text("**𝗦𝘁𝗼𝗽𝗽𝗲𝗱**🚦", True)
    await log_to_channel(bot, f"#BOT_STOPPED\nBy: {m.from_user.id}")
    os.execl(sys.executable, sys.executable, *sys.argv)

@bot.on_message(filters.command("restart"))
async def restart_handler(_, m):
    if not is_authorized(m.from_user.id):
        await m.reply_text("**🚫 You are not authorized to use this command.**")
        return
    await m.reply_text("🔮Restarted🔮", True)
    await log_to_channel(bot, f"#BOT_RESTARTED\nBy: {m.from_user.id}")
    os.execl(sys.executable, sys.executable, *sys.argv)

COOKIES_FILE_PATH = "youtube_cookies.txt"

@bot.on_message(filters.command("cookies") & filters.private)
async def cookies_handler(client: Client, m: Message):
    if not is_authorized(m.from_user.id):
        await m.reply_text("🚫 You are not authorized to use this command.")
        return
        
    await m.reply_text("𝗣𝗹𝗲𝗮𝘀𝗲 𝗨𝗽𝗹𝗼𝗮𝗱 𝗧𝗵𝗲 𝗖𝗼𝗼𝗸𝗶𝗲𝘀 𝗙𝗶𝗹𝗲 (.𝘁𝘅𝘁 𝗳𝗼𝗿𝗺𝗮𝘁).", quote=True)

    try:
        input_message: Message = await client.listen(m.chat.id)

        if not input_message.document or not input_message.document.file_name.endswith(".txt"):
            await m.reply_text("Invalid file type. Please upload a .txt file.")
            return

        downloaded_path = await input_message.download()

        with open(downloaded_path, "r") as uploaded_file:
            cookies_content = uploaded_file.read()

        with open(COOKIES_FILE_PATH, "w") as target_file:
            target_file.write(cookies_content)

        await input_message.reply_text("✅ 𝗖𝗼𝗼𝗸𝗶𝗲𝘀 𝗨𝗽𝗱𝗮𝘁𝗲𝗱 𝗦𝘂𝗰𝗰𝗲𝘀𝘀𝗳𝘂𝗹𝗹𝘆.\n\𝗻📂 𝗦𝗮𝘃𝗲𝗱 𝗜𝗻 youtube_cookies.txt.")
        await log_to_channel(bot, f"#COOKIES_UPDATED\nBy: {m.from_user.id}")
    except Exception as e:
        await m.reply_text(f"⚠️ An error occurred: {str(e)}")

# Define paths for uploaded file and processed file
UPLOAD_FOLDER = '/path/to/upload/folder'
EDITED_FILE_PATH = '/path/to/save/edited_output.txt'

@bot.on_message(filters.command('e2t'))
async def edit_txt(client, message: Message):
    if not is_authorized(message.from_user.id):
        await message.reply_text("🚫 You are not authorized to use this command.")
        return

    await message.reply_text(
        "🎉 **Welcome to the .txt File Editor!**\n\n"
        "Please send your `.txt` file containing subjects, links, and topics."
    )

    input_message: Message = await bot.listen(message.chat.id)
    if not input_message.document:
        await message.reply_text("🚨 **Error**: Please upload a valid `.txt` file.")
        return

    file_name = input_message.document.file_name.lower()
    uploaded_file_path = os.path.join(UPLOAD_FOLDER, file_name)
    uploaded_file = await input_message.download(uploaded_file_path)

    await message.reply_text(
        "🔄 **Send your .txt file name, or type 'd' for the default file name.**"
    )

    user_response: Message = await bot.listen(message.chat.id)
    if user_response.text:
        user_response_text = user_response.text.strip().lower()
        if user_response_text == 'd':
            final_file_name = file_name
        else:
            final_file_name = user_response_text + '.txt'
    else:
        final_file_name = file_name

    try:
        with open(uploaded_file, 'r', encoding='utf-8') as f:
            content = f.readlines()
    except Exception as e:
        await message.reply_text(f"🚨 **Error**: Unable to read the file.\n\nDetails: {e}")
        return

    subjects = {}
    current_subject = None
    for line in content:
        line = line.strip()
        if line and ":" in line:
            title, url = line.split(":", 1)
            title, url = title.strip(), url.strip()

            if title in subjects:
                subjects[title]["links"].append(url)
            else:
                subjects[title] = {"links": [url], "topics": []}

            current_subject = title
        elif line.startswith("-") and current_subject:
            subjects[current_subject]["topics"].append(line.strip("- ").strip())

    sorted_subjects = sorted(subjects.items())
    for title, data in sorted_subjects:
        data["topics"].sort()

    try:
        final_file_path = os.path.join(UPLOAD_FOLDER, final_file_name)
        with open(final_file_path, 'w', encoding='utf-8') as f:
            for title, data in sorted_subjects:
                for link in data["links"]:
                    f.write(f"{title}:{link}\n")
                for topic in data["topics"]:
                    f.write(f"- {topic}\n")
    except Exception as e:
        await message.reply_text(f"🚨 **Error**: Unable to write the edited file.\n\nDetails: {e}")
        return

    try:
        await message.reply_document(
            document=final_file_path,
            caption="📥**𝗘𝗱𝗶𝘁𝗲𝗱 𝗕𝘆 ➤ Gaurav**"
        )
        await log_to_channel(bot, f"#TXT_EDITED\nBy: {message.from_user.id}")
    except Exception as e:
        await message.reply_text(f"🚨 **Error**: Unable to send the file.\n\nDetails: {e}")
    finally:
        if os.path.exists(uploaded_file_path):
            os.remove(uploaded_file_path)

from pytube import Playlist
import youtube_dl

# --- Configuration ---
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# --- Utility Functions ---

def sanitize_filename(name):
    return re.sub(r'[^\w\s-]', '', name).strip().replace(' ', '_')

def get_videos_with_ytdlp(url):
    ydl_opts = {
        'quiet': True,
        'extract_flat': True,
        'skip_download': True,
    }
    try:
        with YoutubeDL(ydl_opts) as ydl:
            result = ydl.extract_info(url, download=False)
            if 'entries' in result:
                title = result.get('title', 'Unknown Title')
                videos = {}
                for entry in result['entries']:
                    video_url = entry.get('url', None)
                    video_title = entry.get('title', None)
                    if video_url:
                        videos[video_title if video_title else "Unknown Title"] = video_url
                return title, videos
            return None, None
    except Exception as e:
        logging.error(f"Error retrieving videos: {e}")
        return None, None

def save_to_file(videos, name):
    filename = f"{sanitize_filename(name)}.txt"
    with open(filename, 'w', encoding='utf-8') as file:
        for title, url in videos.items():
            if title == "Unknown Title":
                file.write(f"{url}\n")
            else:
                file.write(f"{title}: {url}\n")
    return filename

# --- Bot Command ---

@bot.on_message(filters.command('yt2txt'))
async def ytplaylist_to_txt(client: Client, message: Message):
    user_id = message.chat.id
    if user_id != OWNER_ID:
        await message.reply_text("**🚫 You are not authorized to use this command.\n\n🫠 This Command is only for owner.**")
        return

    await message.delete()
    editable = await message.reply_text("📥 **Please enter the YouTube Playlist Url :**")
    input_msg = await client.listen(editable.chat.id)
    youtube_url = input_msg.text
    await input_msg.delete()
    await editable.delete()

    title, videos = get_videos_with_ytdlp(youtube_url)
    if videos:
        file_name = save_to_file(videos, title)
        await message.reply_document(
            document=file_name, 
            caption=f"`{title}`\n\n📥 𝗘𝘅𝘁𝗿𝗮𝗰𝘁𝗲𝗱 𝗕𝘆 ➤ Devil"
        )
        await log_to_channel(bot, f"#YT2TXT\nURL: {youtube_url}\nBy: {message.from_user.id}")
        os.remove(file_name)
    else:
        await message.reply_text("⚠️ **Unable to retrieve videos. Please check the URL.**")

# List users command
@bot.on_message(filters.command("userlist") & filters.user(SUDO_USERS))
async def list_users(client: Client, msg: Message):
    if SUDO_USERS:
        users_list = "\n".join([f"User ID : `{user_id}`" for user_id in SUDO_USERS])
        await msg.reply_text(f"SUDO_USERS :\n{users_list}")
    else:
        await msg.reply_text("No sudo users.")

# Sudo add command
@bot.on_message(filters.command(["sudo"]))
async def sudo_command(client: Client, message: Message):
    # Check if user is owner
    if message.from_user.id != OWNER_ID:
        await message.reply_text("🚫 **This command is only for the owner!**")
        return
        
    if len(message.command) < 3:
        await message.reply_text("⚠️ **Usage:** `/sudo add/remove USER_ID`")
        return
        
    action = message.command[1].lower()
    try:
        user_id = int(message.command[2])
    except ValueError:
        await message.reply_text("❌ **Invalid user ID format. It should be a number.**")
        return
        
    if action == "add":
        if user_id not in SUDO_USERS:
            SUDO_USERS.append(user_id)
            await message.reply_text(f"✅ **User `{user_id}` added to sudo users!**")
            await log_to_channel(bot, f"#SUDO_ADDED\nUser: {user_id}\nBy: {message.from_user.id}")
        else:
            await message.reply_text(f"ℹ️ **User `{user_id}` is already a sudo user.**")
    elif action == "remove":
        if user_id in SUDO_USERS:
            SUDO_USERS.remove(user_id)
            await message.reply_text(f"✅ **User `{user_id}` removed from sudo users!**")
            await log_to_channel(bot, f"#SUDO_REMOVED\nUser: {user_id}\nBy: {message.from_user.id}")
        else:
            await message.reply_text(f"ℹ️ **User `{user_id}` is not a sudo user.**")
    else:
        await message.reply_text("⚠️ **Usage:** `/sudo add/remove USER_ID`")

# Premium user commands
@bot.on_message(filters.command(["addpremium"]))
async def add_premium_command(client: Client, message: Message):
    # Check if user is owner
    if message.from_user.id != OWNER_ID:
        await message.reply_text("🚫 **This command is only for the owner!**")
        return
        
    if len(message.command) < 2:
        await message.reply_text("⚠️ **Usage:** `/addpremium USER_ID`")
        return
        
    try:
        user_id = int(message.command[1])
    except ValueError:
        await message.reply_text("❌ **Invalid user ID format. It should be a number.**")
        return
        
    if is_premium_user(user_id):
        await message.reply_text(f"ℹ️ **User `{user_id}` is already a premium user.**")
        return
        
    await add_premium_user(user_id, 30)  # Add for 30 days by default
    await message.reply_text(f"✅ **User `{user_id}` added as premium user!**")
    await log_to_channel(bot, f"#PREMIUM_ADDED\nUser: {user_id}\nBy: {message.from_user.id}")

@bot.on_message(filters.command(["removepremium"]))
async def remove_premium_command(client: Client, message: Message):
    # Check if user is owner
    if message.from_user.id != OWNER_ID:
        await message.reply_text("🚫 **This command is only for the owner!**")
        return
        
    if len(message.command) < 2:
        await message.reply_text("⚠️ **Usage:** `/removepremium USER_ID`")
        return
        
    try:
        user_id = int(message.command[1])
    except ValueError:
        await message.reply_text("❌ **Invalid user ID format. It should be a number.**")
        return
        
    if not is_premium_user(user_id):
        await message.reply_text(f"ℹ️ **User `{user_id}` is not a premium user.**")
        return
        
    await remove_premium_user(user_id)
    await message.reply_text(f"✅ **User `{user_id}` removed from premium users!**")
    await log_to_channel(bot, f"#PREMIUM_REMOVED\nUser: {user_id}\nBy: {message.from_user.id}")

@bot.on_message(filters.command(["premiumlist"]))
async def premium_list_command(client: Client, message: Message):
    # Check if user is owner
    if message.from_user.id != OWNER_ID:
        await message.reply_text("🚫 **This command is only for the owner!**")
        return
        
    premium_users = await get_premium_users()
    if premium_users:
        users_list = "\n".join([f"User ID : `{user_id}`" for user_id in premium_users])
        await message.reply_text(f"**Premium Users:**\n{users_list}")
    else:
        await message.reply_text("**No premium users.**")

# Help command
@bot.on_message(filters.command("help"))
async def help_command(client: Client, msg: Message):
    help_text = (
        "`/start` - Start the bot⚡\n\n"
        "`/gaurav` - Download and upload files (sudo)🎬\n\n"
        "`/restart` - Restart the bot🔮\n\n" 
        "`/stop` - Stop ongoing process🛑\n\n"
        "`/cookies` - Upload cookies file🍪\n\n"
        "`/e2t` - Edit txt file📝\n\n"
        "`/yt2txt` - Create txt of yt playlist (owner)🗃️\n\n"
        "`/sudo add` - Add user or group or channel (owner)🎊\n\n"
        "`/sudo remove` - Remove user or group or channel (owner)❌\n\n"
        "`/userlist` - List of sudo user or group or channel📜\n\n"
        "`/addpremium` - Add premium user (owner)💰\n\n"
        "`/removepremium` - Remove premium user (owner)🚫\n\n"
        "`/premiumlist` - List premium users (owner)📋\n\n"
    )
    await msg.reply_text(help_text)

# Upload command handler - Renamed from tushar to Devil
@bot.on_message(filters.command(["Devil"]))
async def upload(bot: Client, m: Message):
    if not is_authorized(m.chat.id):
        await m.reply_text("**🚫You are not authorized to use this bot.**")
        await log_to_channel(bot, f"#UNAUTHORIZED_ACCESS\nUser: {m.from_user.id} tried to access /Devil")
        return

    editable = await m.reply_text(f"⚡𝗦𝗘𝗡𝗗 𝗧𝗫𝗧 𝗙𝗜𝗟𝗘⚡")
    try:
        input: Message = await bot.listen(editable.chat.id)
        if not input.document or not input.document.file_name.endswith('.txt'):
            await m.reply_text("😶𝗣𝗹𝗲𝗮𝘀𝗲 𝘀𝗲𝗻𝗱 𝗮 .𝘁𝘅𝘁 𝗳𝗶𝗹𝗲😶")
            return
            
        x = await input.download()
        await input.delete(True)
        file_name, ext = os.path.splitext(os.path.basename(x))
        pdf_count = 0
        img_count = 0
        zip_count = 0
        video_count = 0
        
        try:    
            with open(x, "r", encoding='utf-8') as f:
                content = f.read()
            content = content.split("\n")
            
            links = []
            for i in content:
                i = i.strip()
                if "://" in i:
                    # Extract URL and clean it properly
                    parts = i.split("://", 1)
                    url_prefix = parts[0] + "://"
                    url = parts[1]
                    
                    # Handle special cases for some URLs
                    if "drive.google.com" in url and "view?usp=sharing" in url:
                        url = url.replace("/view?usp=sharing", "")  # Clean Google Drive links
                    
                    links.append([i.split("://", 1)[0], url])
                    
                    # Categorize link type for counting
                    if ".pdf" in url.lower():
                        pdf_count += 1
                    elif any(url.lower().endswith(ext) for ext in [".png", ".jpeg", ".jpg", ".gif"]):
                        img_count += 1
                    elif ".zip" in url.lower():
                        zip_count += 1
                    else:
                        video_count += 1
            os.remove(x)
        except UnicodeDecodeError:
            await m.reply_text("😶𝗜𝗻𝘃𝗮𝗹𝗶𝗱 𝗙𝗶𝗹𝗲 𝗘𝗻𝗰𝗼𝗱𝗶𝗻𝗴😶\n\n𝗣𝗹𝗲𝗮𝘀𝗲 𝗺𝗮𝗸𝗲 𝘀𝘂𝗿𝗲 𝘁𝗵𝗲 𝗳𝗶𝗹𝗲 𝗶𝘀 𝗶𝗻 𝗨𝗧𝗙-𝟴 𝗲𝗻𝗰𝗼𝗱𝗶𝗻𝗴")
            os.remove(x)
            return
        except Exception as e:
            await m.reply_text(f"😶𝗘𝗿𝗿𝗼𝗿 𝗽𝗿𝗼𝗰𝗲𝘀𝘀𝗶𝗻�� 𝗳𝗶𝗹𝗲😶\n\n𝗘𝗿𝗿𝗼𝗿: {str(e)}")
            os.remove(x)
            return
        
        await editable.edit(f"`𝗧𝗼𝘁𝗮𝗹 🔗 𝗟𝗶𝗻𝗸𝘀 𝗙𝗼𝘂𝗻𝗱 𝗔𝗿𝗲 {len(links)}\n\n🔹Img : {img_count}  🔹Pdf : {pdf_count}\n🔹Zip : {zip_count}  🔹Video : {video_count}\n\n𝗦𝗲𝗻𝗱 𝗙𝗿𝗼𝗺 𝗪𝗵𝗲𝗿𝗲 𝗼𝘂 𝗪𝗮𝗻𝘁 𝗧𝗼 𝗼𝘄𝗻𝗹𝗼𝗮𝗱.`")
        input0: Message = await bot.listen(editable.chat.id)
        raw_text = input0.text
        await input0.delete(True)
        try:
            arg = int(raw_text)
        except:
            arg = 1
        await editable.edit("📚 𝗘𝗻𝘁𝗲𝗿 𝗬𝗼𝘂𝗿 𝗕𝗮𝘁𝗰𝗵 𝗡𝗮𝗺𝗲 📚\n\n🦠 𝗦𝗲𝗻𝗱 `1` 𝗙𝗼𝗿 𝗨𝘀𝗲 𝗗𝗲𝗳𝗮𝘂𝗹𝘁 🦠")
        input1: Message = await bot.listen(editable.chat.id)
        raw_text0 = input1.text
        await input1.delete(True)
        if raw_text0 == '1':
            b_name = file_name
        else:
            b_name = raw_text0
        
        await editable.edit("**📸 𝗘𝗻𝘁𝗲𝗿 𝗥𝗲𝘀𝗼𝗹𝘂𝘁𝗶𝗼𝗻 📸**\n➤ `144`\n➤ `240`\n➤ `360`\n➤ `480`\n➤ `720`\n➤ `1080`")
        input2: Message = await bot.listen(editable.chat.id)
        raw_text2 = input2.text
        await input2.delete(True)
        try:
            if raw_text2 == "144":
                res = "256x144"
            elif raw_text2 == "240":
                res = "426x240"
            elif raw_text2 == "360":
                res = "640x360"
            elif raw_text2 == "480":
                res = "854x480"
            elif raw_text2 == "720":
                res = "1280x720"
            elif raw_text2 == "1080":
                res = "1920x1080" 
            else: 
                res = "UN"
        except Exception:
                res = "UN"
        
        await editable.edit("📛 𝗘𝗻𝘁𝗲𝗿 𝗬𝗼𝘂𝗿 𝗡𝗮𝗺𝗲 📛\n\n🐥 𝗦𝗲𝗻𝗱 `1` 𝗙𝗼𝗿 𝗨𝘀𝗲 𝗗𝗲𝗳𝗮𝘂𝗹𝘁 🐥")
        input3: Message = await bot.listen(editable.chat.id)
        raw_text3 = input3.text
        await input3.delete(True)
        credit = "[Gaurav](https://t.me/ytbr_67)"
        if raw_text3 == '1':
            CR = "[Gaurav](https://t.me/ytbr_67)"
        elif raw_text3:
            try:
                text, link = raw_text3.split(',')
                CR = f'[{text.strip()}]({link.strip()})'
            except ValueError:
                CR = raw_text3
        else:
            CR = credit
       
        await editable.edit("**𝗘𝗻𝘁𝗲𝗿 𝗣𝘄 𝗧𝗼𝗸𝗲𝗻 𝗙𝗼𝗿 𝗣𝘄 𝗨𝗽𝗹𝗼𝗮𝗱𝗶𝗻𝗴 𝗼𝗿 𝗦𝗲𝗻𝗱 `3` 𝗙𝗼𝗿 𝗢𝘁𝗵𝗲𝗿𝘀**")
        input4: Message = await bot.listen(editable.chat.id)
        raw_text4 = input4.text
        await input4.delete(True)
        if raw_text4 == 3:
            MR = token
        else:
            MR = raw_text4
        
        await editable.edit("𝗡𝗮𝗲 𝗦𝗲𝗻𝗱 𝗧𝗵𝗲 𝗧𝗵𝘂𝗺𝗯 𝗨𝗿𝗹 𝗘𝗴 » https://graph.org/file/13a89d77002442255efad-989ac290c1b3f13b44.jpg\n\n𝗢𝗿 𝗜𝗳 𝗗𝗼𝗻'𝘁 𝗪𝗮𝗻𝘁 𝗧𝗵𝘂𝗺𝗯𝗻𝗮𝗶 𝗦𝗲𝗻𝗱 = 𝗻𝗼")
        input6 = message = await bot.listen(editable.chat.id)
        raw_text6 = input6.text
        await input6.delete(True)
        await editable.delete()

        thumb = input6.text
        if thumb.startswith("http://") or thumb.startswith("https://"):
            getstatusoutput(f"wget '{thumb}' -O 'thumb.jpg'")
            thumb = "thumb.jpg"
        else:
            thumb == "no"
        failed_count =0
        
        if len(links) == 1:
            count = 1
        else:
            count = int(raw_text)

        try:
            for i in range(count - 1, len(links)):
                V = links[i][1].replace("file/d/","uc?export=download&id=").replace("www.youtube-nocookie.com/embed", "youtu.be").replace("?modestbranding=1", "").replace("/view?usp=sharing","")
                url = "https://" + V

                if "visionias" in url:
                    async with ClientSession() as session:
                        async with session.get(url, headers={'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9', 'Accept-Language': 'en-US,en;q=0.9', 'Cache-Control': 'no-cache', 'Connection': 'keep-alive', 'Pragma': 'no-cache', 'Referer': 'http://www.visionias.in/', 'Sec-Fetch-Dest': 'iframe', 'Sec-Fetch-Mode': 'navigate', 'Sec-Fetch-Site': 'cross-site', 'Upgrade-Insecure-Requests': '1', 'User-Agent': 'Mozilla/5.0 (Linux; Android 12; RMX2121) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36', 'sec-ch-ua': '"Chromium";v="107", "Not=A?Brand";v="24"', 'sec-ch-ua-mobile': '?1', 'sec-ch-ua-platform': '"Android"',}) as resp:
                            text = await resp.text()
                            url = re.search(r"(https://.*?playlist.m3u8.*?)\"", text).group(1)
                            
                elif 'media-cdn.classplusapp.com/drm/' in url:
                    url = f"https://dragoapi.vercel.app/video/{url}"

                elif "https://appx-transcoded-videos.livelearn.in/videos/rozgar-data/" in url:
                    url = url.replace("https://appx-transcoded-videos.livelearn.in/videos/rozgar-data/", "")
                    name1 = links[i][0].replace("\t", "").replace(":", "").replace("/", "").replace("+", "").replace("#", "").replace("|", "").replace("@", "@").replace("*", "").replace(".", "").replace("https", "").replace("http", "").strip()
                    name = f'{str(count).zfill(3)}) {name1[:60]}'
                    cmd = f'yt-dlp -o "{name}.mp4" "{url}"'
                    
                elif "videos.classplusapp" in url:
                    url = requests.get(f'https://api.classplusapp.com/cams/uploader/video/jw-signed-url?url={url}', headers={'x-access-token': 'eyJjb3Vyc2VJZCI6IjQ1NjY4NyIsInR1dG9ySWQiOm51bGwsIm9yZ0lkIjo0ODA2MTksImNhdGVnb3J5SWQiOm51bGx9'}).json()['url']
                    
                elif "tencdn.classplusapp" in url or "media-cdn-alisg.classplusapp.com" in url or "media-cdn.classplusapp" in url:
                    headers = {'Host': 'api.classplusapp.com', 'x-access-token': 'eyJjb3Vyc2VJZCI6IjQ1NjY4NyIsInR1dG9ySWQiOm51bGwsIm9yZ0lkIjo0ODA2MTksImNhdGVnb3J5SWQiOm51bGx9', 'user-agent': 'Mobile-Android', 'app-version': '1.4.37.1', 'api-version': '18', 'device-id': '5d0d17ac8b3c9f51', 'device-details': '2848b866799971ca_2848b8667a33216c_SDK-30', 'accept-encoding': 'gzip'}
                    params = (('url', f'{url}'),)
                    response = requests.get('https://api.classplusapp.com/cams/uploader/video/jw-signed-url', headers=headers, params=params)
                    url = response.json()['url']

                elif "https://appx-transcoded-videos-mcdn.akamai.net.in/videos/bhainskipathshala-data/" in url:
                    url = url.replace("https://appx-transcoded-videos-mcdn.akamai.net.in/videos/bhainskipathshala-data/", "")
                    name1 = links[i][0].replace("\t", "").replace(":", "").replace("/", "").replace("+", "").replace("#", "").replace("|", "").replace("@", "@").replace("*", "").replace(".", "").replace("https", "").replace("http", "").strip()
                    name = f'{str(count).zfill(3)}) {name1[:60]}'
                    cmd = f'yt-dlp -o "{name}.mp4" "{url}"'

                elif "apps-s3-jw-prod.utkarshapp.com" in url:
                    if 'enc_plain_mp4' in url:
                        url = url.replace(url.split("/")[-1], res+'.mp4')
                        
                    elif 'Key-Pair-Id' in url:
                        url = None
                        
                    elif '.m3u8' in url:
                        q = ((m3u8.loads(requests.get(url).text)).data['playlists'][1]['uri']).split("/")[0]
                        x = url.split("/")[5]
                        x = url.replace(x, "")
                        url = ((m3u8.loads(requests.get(url).text)).data['playlists'][1]['uri']).replace(q+"/", x)
                
                elif "/master.mpd" in url or "d1d34p8vz63oiq" in url or "sec1.pw.live" in url:
                    id = url.split("/")[-2]
                    url = f"https://anonymouspwplayer-b99f57957198.herokuapp.com/pw?url={url}?token={raw_text4}"
                
                name1 = links[i][0].replace("\t", "").replace(":", "").replace("/", "").replace("+", "").replace("#", "").replace("|", "").replace("@", "").replace("*", "").replace(".", "").replace("https", "").replace("http", "").strip()
                name = f'{str(count).zfill(3)}) {name1[:60]}'

                if 'khansirvod4.pc.cdn.bitgravity.com' in url:               
                    parts = url.split('/')               
                    part1 = parts[1]
                    part2 = parts[2]
                    part3 = parts[3] 
                    part4 = parts[4]
                    part5 = parts[5]
                    
                    print(f"PART1: {part1}")
                    print(f"PART2: {part2}")
                    print(f"PART3: {part3}")
                    print(f"PART4: {part4}")
                    print(f"PART5: {part5}")
                    url = f"https://kgs-v4.akamaized.net/kgs-cv/{part3}/{part4}/{part5}"
               
                if "youtu" in url:
                    ytf = f"b[height<={raw_text2}][ext=mp4]/bv[height<={raw_text2}][ext=mp4]+ba[ext=m4a]/b[ext=mp4]"
                else:
                    ytf = f"b[height<={raw_text2}]/bv[height<={raw_text2}]+ba/b/bv+ba"
              
                if "edge.api.brightcove.com" in url:
                    bcov = 'bcov_auth=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpYXQiOjE3MzUxMzUzNjIsImNvbiI6eyJpc0FkbWluIjpmYWxzZSwiYXVzZXIiOiJVMFZ6TkdGU2NuQlZjR3h5TkZwV09FYzBURGxOZHowOSIsImlkIjoiYmt3cmVIWmxZMFUwVXpkSmJYUkxVemw2ZW5Oclp6MDkiLCJmaXJzdF9uYW1lIjoiY25GdVpVdG5kRzR4U25sWVNGTjRiVW94VFhaUVVUMDkiLCJlbWFpbCI6ImFFWllPRXhKYVc1NWQyTlFTazk0YmtWWWJISTNRM3BKZW1OUVdIWXJWWE0wWldFNVIzZFNLelE0ZHowPSIsInBob25lIjoiZFhSNlFrSm9XVlpCYkN0clRUWTFOR3REU3pKTVVUMDkiLCJhdmF0YXIiOiJLM1ZzY1M4elMwcDBRbmxrYms4M1JEbHZla05pVVQwOSIsInJlZmVycmFsX2NvZGUiOiJhVVZGZGpBMk9XSnhlbXRZWm14amF6TTBVazQxUVQwOSIsImRldmljZV90eXBlIjoid2ViIiwiZGV2aWNlX3ZlcnNpb24iOiJDaHJvbWUrMTE5IiwiZGV2aWNlX21vZGVsIjoiY2hyb21lIiwicmVtb3RlX2FkZHIiOiIyNDA5OjQwYzI6MjA1NTo5MGQ0OjYzYmM6YTNjOTozMzBiOmIxOTkifX0.Kifitj1wCe_ohkdclvUt7WGuVBsQFiz7eezXoF1RduDJi4X7egejZlLZ0GCZmEKBwQpMJLvrdbAFIRniZoeAxL4FZ-pqIoYhH3PgZU6gWzKz5pdOCWfifnIzT5b3rzhDuG7sstfNiuNk9f-HMBievswEIPUC_ElazXdZPPt1gQqP7TmVg2Hjj6-JBcG7YPSqa6CUoXNDHpjWxK_KREnjWLM7vQ6J3vF1b7z_S3_CFti167C6UK5qb_turLnOUQzWzcwEaPGB3WXO0DAri6651WF33vzuzeclrcaQcMjum8n7VQ0Cl3fqypjaWD30btHQsu5j8j3pySWUlbyPVDOk-g'
                    url = url.split("bcov_auth")[0]+bcov
                
                if "jw-prod" in url:
                    cmd = f'yt-dlp -o "{name}.mp4" "{url}"'
                
                elif "webvideos.classplusapp." in url:
                   cmd = f'yt-dlp --add-header "referer:https://web.classplusapp.com/" --add-header "x-cdn-tag:empty" -f "{ytf}" "{url}" -o "{name}.mp4"'
                
                elif "youtube.com" in url or "youtu.be" in url:
                    cmd = f'yt-dlp --cookies youtube_cookies.txt -f "bestvideo[height<={raw_text2}]+bestaudio/best[height<={raw_text2}]" "{url}" -o "{name}.mp4"'
                
                else:
                    # Generic fallback for other URLs
                    cmd = f'yt-dlp -f "best" "{url}" -o "{name}.mp4"'

                try:  
                    cc = f'**[🎬] 𝗩𝗶𝗱_𝗜𝗱 : {str(count).zfill(3)}.\n\n\n☘️𝗧𝗶𝘁𝗹𝗲 𝗡𝗮𝗺𝗲 ➤ {name1}.({res}).Gaurav.mkv\n\n\n<pre><code>📚𝗕𝗮𝘁𝗰𝗵 𝗡𝗮𝗺𝗲 ➤ {b_name}</code></pre>\n\n\n📥 𝗘𝘅𝘁𝗿𝗮𝗰𝘁𝗲𝗱 𝗕𝘆 ➤  {CR}**'
                    cpvod = f'**[🎬] 𝗩𝗶𝗱_𝗜𝗱 : {str(count).zfill(3)}.\n\n\n☘️𝗧𝗶𝘁𝗹𝗲 𝗡𝗮𝗺𝗲 ➤ {name1}.({res}).Gaurav.mkv\n\n\n🔗𝗩𝗶𝗱𝗲𝗼 𝗨𝗿𝗹 ➤ <a href="{url}">__Click Here to Watch Video__</a>\n\n\n<pre><code>📚𝗕𝗮𝘁𝗰𝗵 𝗡𝗮𝗺𝗲 ➤ {b_name}</code></pre>\n\n\n📥 𝗘𝘅𝘁𝗿𝗮𝗰𝘁𝗲𝗱 𝗕𝘆 ➤  {CR}**'
                    cimg = f'**[📁] 𝗜𝗺𝗴_𝗜𝗱 : {str(count).zfill(3)}.\n\n\n☘️𝗧𝗶𝘁𝗹𝗲 𝗡𝗮𝗺𝗲 ➤ {name1}.Gaurav.jpg\n\n\n<pre><code>📚𝗕𝗮𝘁𝗰𝗵 𝗡𝗮𝗺𝗲 ➤ {b_name}</code></pre>\n\n\n📥 𝗘𝘅𝘁𝗿𝗮𝗰𝘁𝗲𝗱 𝗕𝘆 ➤  {CR}**'
                    cczip = f'**[📁] 𝗣𝗱𝗳_𝗜𝗱 : {str(count).zfill(3)}.\n\n\n☘️𝗧𝗶𝘁𝗹𝗲 𝗡𝗮𝗺𝗲 ➤ {name1}.Gaurav.zip\n\n\n<pre><code>📚𝗕𝗮𝘁𝗰𝗵 𝗡𝗮𝗺𝗲 ➤ {b_name}</code></pre>\n\n\n📥 𝗘𝘅𝘁𝗿𝗮𝗰𝘁𝗲𝗱 𝗕𝘆 ➤  {CR}**'
                    cc1 = f'**[📁] 𝗣𝗱𝗳_𝗜𝗱 : {str(count).zfill(3)}.\n\n\n☘️𝗧𝗶𝘁𝗹𝗲 𝗡𝗮𝗺𝗲 ➤ {name1}.Gaurav.pdf\n\n\n<pre><code>📚𝗕𝗮𝘁𝗰𝗵 𝗡𝗮𝗺𝗲 ➤ {b_name}</code></pre>\n\n\n📥 𝗘𝘅𝘁𝗿𝗮𝗰𝘁��𝗱 𝗕𝘆 ➤  {CR}**'
              
                    if "drive" in url:
                        try:
                            ka = await helper.download(url, name)
                            copy = await bot.send_document(chat_id=m.chat.id,document=ka, caption=cc1)
                            count+=1
                            os.remove(ka)
                            time.sleep(1)
                        except FloodWait as e:
                            await m.reply_text(str(e))
                            time.sleep(e.x)
                            continue

                    elif ".pdf" in url:
                        try:
                            await asyncio.sleep(4)
                            url = url.replace(" ", "%20")
                            scraper = cloudscraper.create_scraper()
                            response = scraper.get(url)

                            if response.status_code == 200:
                                with open(f'{name}.pdf', 'wb') as file:
                                    file.write(response.content)

                                await asyncio.sleep(4)
                                copy = await bot.send_document(chat_id=m.chat.id, document=f'{name}.pdf', caption=cc1)
                                count += 1
                                os.remove(f'{name}.pdf')
                            else:
                                await m.reply_text(f"Failed to download PDF: {response.status_code} {response.reason}")

                        except FloodWait as e:
                            await m.reply_text(str(e))
                            time.sleep(e.x)
                            continue
                            
                    elif "media-cdn.classplusapp.com/drm/" in url:
                        try:
                            await bot.send_photo(chat_id=m.chat.id, photo=cpimg, caption=cpvod)
                            count +=1
                        except Exception as e:
                            await m.reply_text(str(e))    
                            time.sleep(1)    
                            continue          
                            
                    elif any(ext in url.lower() for ext in [".jpg", ".jpeg", ".png"]):
                        try:
                            await asyncio.sleep(4)
                            url = url.replace(" ", "%20")
                            scraper = cloudscraper.create_scraper()
                            response = scraper.get(url)

                            if response.status_code == 200:
                                with open(f'{name}.jpg', 'wb') as file:
                                    file.write(response.content)

                                await asyncio.sleep(2)
                                copy = await bot.send_photo(chat_id=m.chat.id, photo=f'{name}.jpg', caption=cimg)
                                count += 1
                                os.remove(f'{name}.jpg')

                            else:
                                await m.reply_text(f"Failed to download Image: {response.status_code} {response.reason}")

                        except FloodWait as e:
                            await m.reply_text(str(e))
                            await asyncio.sleep(2)
                            return  
                        
                        except Exception as e:
                            await m.reply_text(f"An error occurred: {str(e)}")
                            await asyncio.sleep(4)
                            
                    elif ".zip" in url:
                        try:
                            cmd = f'yt-dlp -o "{name}.zip" "{url}"'
                            download_cmd = f"{cmd} -R 25 --fragment-retries 25"
                            os.system(download_cmd)
                            copy = await bot.send_document(chat_id=m.chat.id, document=f'{name}.zip', caption=cczip)
                            count += 1
                            os.remove(f'{name}.zip')
                        except FloodWait as e:
                            await m.reply_text(str(e))
                            time.sleep(e.x)
                            count += 1
                            continue
                            
                    elif ".pdf" in url:
                        try:
                            cmd = f'yt-dlp -o "{name}.pdf" "{url}"'
                            download_cmd = f"{cmd} -R 25 --fragment-retries 25"
                            os.system(download_cmd)
                            copy = await bot.send_document(chat_id=m.chat.id, document=f'{name}.pdf', caption=cc1)
                            count += 1
                            os.remove(f'{name}.pdf')
                        except FloodWait as e:
                            await m.reply_text(str(e))
                            time.sleep(e.x)
                            continue
                    else:
                        emoji_message = await show_random_emojis(message)
                        remaining_links = len(links) - count
                        Show = f"**🍁 𝗗𝗢𝗪𝗡𝗟𝗢𝗔𝗗𝗜𝗡 🍁**\n\n**📝ɴᴀᴍᴇ » ** `{name}\n\n🔗ᴛᴏᴛᴀʟ ᴜʀʟ » {len(links)}\n\n🗂️ɪɴᴅᴇx » {str(count)}/{len(links)}\n\n🌐ʀᴇᴍᴀɪɴɪɴɢ ᴜʀʟ » {remaining_links}\n\n❄ǫᴜᴀʟɪᴛʏ » {res}`\n\n**🔗ᴜʀʟ » ** `{url}`\n\n🤖𝗕𝗢𝗧 𝗠𝗔𝗗𝗘 𝗕𝗬 ➤ Devil\n\n🙂 चलो फिर से अजनबी बन जायें 🙂"
                        prog = await m.reply_text(Show)
                        res_file = await helper.download_video(url, cmd, name)
                        filename = res_file
                        await prog.delete(True)
                        await emoji_message.delete()
                        await helper.send_vid(bot, m, cc, filename, thumb, name, prog)
                        count += 1
                        time.sleep(1)

                except Exception as e:
                    await m.reply_text(f'‼️ **DOWNLOAD FAILED** ‼️\n\n'
                                       f'📝 **Name:** `{name}`\n\n'
                                       f'🔗 **URL:** <a href="{url}">Click Here to See Link</a>\n\n'
                                       f'❌ **Error:** `{str(e)[:200]}`')
                                   
                    count += 1
                    failed_count += 1
                    continue   

        except Exception as e:
            await m.reply_text(e)
            await log_to_channel(bot, f"#ERROR\nError in /gaurav command\nError: {str(e)}\nBy: {m.from_user.id}")
        
        await m.reply_text(f"`✨𝗕𝗔𝗧𝗖𝗛 𝗦𝗨𝗠𝗠𝗔𝗥𝗬✨\n\n"
                           f"▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n"
                           f"��𝗜𝗻𝗱𝗲𝘅 𝗥𝗮𝗻𝗴𝗲 » ({raw_text} to {len(links)})\n"
                           f"📚��𝗮𝘁𝗰𝗵 𝗡𝗮𝗺𝗲 » {b_name}\n\n"
                           f"▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n"
                           f"✨𝗧𝗫𝗧 𝗦𝗨𝗠𝗠𝗔𝗥𝗬✨ : {len(links)}\n"
                           f"▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n"
                           f"🔹𝗩𝗶𝗱𝗲𝗼 » {video_count}\n🔹𝗣𝗱𝗳 » {pdf_count}\n🔹𝗜𝗺𝗴 » {img_count}\n🔹𝗭𝗶𝗽 » {zip_count}\n🔹𝗙𝗮𝗶𝗹𝗲𝗱 𝗨𝗿𝗹 » {failed_count}\n\n"
                           f"▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n"
                           f"✅𝗦𝗧𝗔𝗧��𝗦 » 𝗖𝗢𝗠𝗣𝗟𝗘𝗧𝗘𝗗`")
        await m.reply_text(f"<pre><code>��𝗘𝘅𝘁𝗿𝗮𝗰𝘁𝗲𝗱 𝗕𝘆 ➤『{CR}』</code></pre>")
        await m.reply_text(f"<pre><code>『😏𝗥��𝗮𝗰𝘁𝗶𝗼𝗻 𝗞𝗼𝗻 𝗗𝗲𝗴𝗮😏』</code></pre>")
        await log_to_channel(bot, f"#BATCH_COMPLETED\nUser: {m.from_user.id}\nBatch: {b_name}\nTotal: {len(links)}\nFailed: {failed_count}")

    except Exception as e:
        await m.reply_text(e)
        await log_to_channel(bot, f"#ERROR\nError in /gaurav command\nError: {str(e)}\nBy: {m.from_user.id}")

if __name__ == "__main__":
    logger.info("Starting bot...")
    bot.run()
