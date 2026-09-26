import os
import sys

import discord
from discord.ext import commands

from utils.db import init_db

TOKEN = os.getenv("DISCORD_TOKEN")
OWNER_IDS = {
    123456789012345678,
    987654321098765432,
}

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
intents.voice_states = True

bot = commands.Bot(
    command_prefix="!",
    intents=intents,
    help_command=None,
)


@bot.event
async def on_ready():
    init_db()
    print(f"Bot connecté : {bot.user} ({bot.user.id})")
    print(f"Serveurs : {len(bot.guilds)}")
    await bot.tree.sync()
    print("Slash commands synchronisées.")


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
    for filename in os.listdir("cogs"):
        if filename.endswith(".py") and not filename.startswith("__"):
            module_name = f"cogs.{filename[:-3]}"
            try:
                await bot.load_extension(module_name)
                print(f"Chargé : {module_name}")
            except Exception as exc:
                print(f"Erreur lors du chargement de {module_name}: {exc}")


async def main():
    await load_extensions()
    if not TOKEN:
        print("Erreur : DISCORD_TOKEN non défini.")
        print("Ajoute la variable d'environnement DISCORD_TOKEN.")
        sys.exit(1)
    await bot.start(TOKEN)


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
