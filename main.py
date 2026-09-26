import os
import sys
import asyncio

import discord
from discord.ext import commands

from config import DISCORD_TOKEN, BOT_PREFIX, BOT_ACTIVITY, ENABLE_MEMBERS, ENABLE_MESSAGE_CONTENT
from utils.db import init_db


intents = discord.Intents.default()
intents.members = ENABLE_MEMBERS
intents.message_content = ENABLE_MESSAGE_CONTENT
intents.voice_states = True

bot = commands.Bot(
    command_prefix=BOT_PREFIX,
    intents=intents,
    help_command=None,
    activity=discord.Activity(type=discord.ActivityType.watching, name=BOT_ACTIVITY or "SITE-453"),
)


@bot.event
async def on_ready():
    init_db()
    print(f"Bot connecté : {bot.user} ({bot.user.id})")
    print(f"Serveurs : {len(bot.guilds)}")
    try:
        await bot.tree.sync()
        print("Slash commands synchronisées.")
    except Exception as exc:
        print(f"Erreur lors de la sync des slash commands : {exc}")


@bot.event
async def on_message(message: discord.Message):
    if message.author.bot:
        return
    if message.guild is None:
        return

    if message.content.startswith(f"<@{bot.user.id}>") or message.content.startswith(f"<@!{bot.user.id}>"):
        await message.channel.send(
            f"Bonjour {message.author.mention}, je suis en ligne. Utilise `/help` pour voir les commandes."
        )

    await bot.process_commands(message)


async def load_extensions():
    for filename in sorted(os.listdir("cogs")):
        if filename.endswith(".py") and not filename.startswith("__"):
            module_name = f"cogs.{filename[:-3]}"
            try:
                await bot.load_extension(module_name)
                print(f"Chargé : {module_name}")
            except Exception as exc:
                print(f"Erreur lors du chargement de {module_name}: {exc}")


async def main():
    await load_extensions()
    if not DISCORD_TOKEN:
        print("Erreur : DISCORD_TOKEN non défini.")
        print("Ajoute la variable d'environnement DISCORD_TOKEN dans ton fichier .env")
        sys.exit(1)
    await bot.start(DISCORD_TOKEN)


if __name__ == "__main__":
    asyncio.run(main())
