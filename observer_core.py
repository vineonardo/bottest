from telegram.ext import ApplicationBuilder
import os
import logging
import discord
import asyncio
from log_matrix import log_message
from signal_score import score_message

from rotating_filter import BloomFilter
bloom = BloomFilter(expected_items=1000)

async def launch_telegram_observer():
    from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
    import os
    import logging

    from log_matrix import log_message
    from signal_score import score_message

    TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
    if not TELEGRAM_TOKEN:
        raise ValueError("TELEGRAM_TOKEN is not set")

    async def handle_message(update, context: ContextTypes.DEFAULT_TYPE):
        if not update.effective_message or not update.effective_chat:
            return

        content = update.effective_message.text or ""

        msg_id = update.effective_message.message_id
        if str(msg_id) in bloom:
            print(f"[TELEGRAM] Skipping duplicate message {msg_id}")
            return
        bloom.add(str(msg_id))
        score = score_message(content)

        data = {
            "platform": "telegram",
            "group_id": update.effective_chat.id,
            "timestamp": update.effective_message.date.isoformat(),
            "user": update.effective_message.from_user.username if update.effective_message.from_user else "unknown",
            "content": content,
            "meta": {
                "msg_id": update.effective_message.message_id,
                "chat_type": update.effective_chat.type,
                "score": score,
                "filtered": score >= 0.4
            },
        }

        await log_message(data)

    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))


    await app.initialize()
    await app.start()
    print("Telegram bot started in background mode.")



intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.messages = True

class DiscordClient(discord.Client):
    def __init__(self, guild_whitelist, **kwargs):
        super().__init__(**kwargs)
        self.guild_whitelist = guild_whitelist

    async def on_ready(self):
        logging.info(f"Discord bot logged in as {self.user}")

    async def on_message(self, message):
        if message.author == self.user:
            return

        if self.guild_whitelist and str(message.guild.id) not in self.guild_whitelist:
            return

        content = message.content or "[non-text message]"

        msg_id = message.id
        if str(msg_id) in bloom:
            print(f"[DISCORD] Skipping duplicate message {msg_id}")
            return
        bloom.add(str(msg_id))

        score = score_message(content)
   
        data = {
            "platform": "discord",
            "group_id": message.channel.id,
            "timestamp": message.created_at.isoformat(),
            "user": str(message.author),
            "content": content,
            "meta": {
                "msg_id": message.id,
                "guild": message.guild.name,
                "channel": message.channel.name,
                "score": score,
                "filtered": score >= 0.4,
            },
        }

        await log_message(data)

async def launch_discord_observer():
    DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
    if not DISCORD_TOKEN:
        raise ValueError("DISCORD_TOKEN is not set.")

    GUILD_WHITELIST = os.getenv("DISCORD_GUILDS", "").split(",")
    GUILD_WHITELIST = [g.strip() for g in GUILD_WHITELIST if g.strip()]

    client = DiscordClient(guild_whitelist=GUILD_WHITELIST, intents=intents)
    print("Discord client created, starting bot...")
    await client.start(DISCORD_TOKEN)
