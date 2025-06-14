import os
from pyrogram import filters
from motor.motor_asyncio import AsyncIOMotorClient
from cachetools import TTLCache, LRUCache

API_ID = int(os.getenv("API_ID", "28164938"))
API_HASH = os.getenv("API_HASH", "d53fd90b87686f713f6adc9428bbb6bb")
BOT_TOKEN = os.getenv("BOT_TOKEN", "8027631028:AAGu7PjgrEajVQC6-ZpClbp_QvUv1XBzikA")
MONGO_URL = os.getenv("MONGO_URL", "mongodb+srv://iamnobita1:nobitamusic1@cluster0.k08op.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
GROUP_IDS = [int(gid.strip()) for gid in os.getenv("GROUP_IDS", "-1002559277065, -1002506225416").split(",")]
START_PIC = os.getenv("START_IMG", "https://files.catbox.moe/6nl03c.jpg")

START_MESSAGE = """
🌟 **Welcome to the Anime Character Guessing Bot!** 🌟

Get ready to test your anime knowledge in an exciting guessing game! 🎮  
Guess the anime characters from images in our supported groups and earn coins for every correct answer! 💰  

This bot is **open-source**, built with ❤️ by the community for anime fans like you! Join the fun, track your streaks, and climb the leaderboards! 🏆  

👇 **Use the buttons below to learn more or start playing!**
- Use `/nguess` in a supported group to begin.
- Join our update channel for news and updates!
- Need help? Hit the Help button or contact the developer.

**Bot Version**: `2.0`  
Made by **𝚴 𝐎 𝐁 𝚰 𝐓 𝚲** | Powered by [𝚴 𝐎 𝐁 𝚰 𝐓 𝚲](https://t.me/ll_NOBITA_DEFAULTERS_ll)
"""

not_command_filter = filters.create(lambda _, __, msg: msg.text and not msg.text.startswith('/'))

COOLDOWN_PERIOD = 4 * 60 * 60
GUESS_TIMEOUT = 5 * 60
MAX_GUESSES = 1000000

client_ddw = AsyncIOMotorClient(MONGO_URL, maxPoolSize=10)
db = client_ddw['hinata_waifu']
user_collection = db['gamimg_user_collection']
collection = db['gaming_anime_characters']

character_cache = LRUCache(maxsize=100)
user_cache = TTLCache(maxsize=1000, ttl=3600)

ongoing_sessions = {}
user_total_guesses = {}
streak_data = {group_id: {"current_streak": 0, "last_correct_user": None} for group_id in GROUP_IDS}

emojis = ["👍", "😘", "❤️", "🔥", "🥰", "🤩", "💘", "😏", "🤯", "⚡️", "🏆", "🤭", "🎉"]

chat_filter = filters.chat(GROUP_IDS)
