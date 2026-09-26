import discord
from discord.ext import commands
from discord import app_commands

from utils.db import user_has_at_least, log_event

OWNER_IDS = {
    123456789012345678,
    987654321098765432,
}

class Announce(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def can_manage(self, interaction: discord.Interaction, required: str = "moderator"):
        if interaction.user.id in OWNER_IDS:
            return True
        return user_has_at_least(interaction.guild.id, interaction.user.id, required, owner_ids=OWNER_IDS)

    @app_commands.command(name="announce", description="Envoie une annonce dans un salon")
    @app_commands.describe(channel="Salon de destination", message="Message à envoyer")
    async def announce_cmd(self, interaction: discord.Interaction, channel: discord.TextChannel, message: str):
        if not self.can_manage(interaction, "moderator"):
            await interaction.response.send_message("❌ Tu n'as pas la permission.", ephemeral=True)
            return

        await channel.send(message)

        embed = discord.Embed(
            title="Annonce envoyée",
            description=f"Message envoyé dans {channel.mention}.",
            color=discord.Color.green()
        )
        await interaction.response.send_message(embed=embed)

        log_event(interaction.guild, "Annonce", f"{interaction.user.mention} a envoyé une annonce dans {channel.mention}.")

    @app_commands.command(name="pm", description="Envoie un message privé à un membre")
    @app_commands.describe(user="Utilisateur", message="Message à envoyer")
    async def pm_cmd(self, interaction: discord.Interaction, user: discord.Member, message: str):
        if not self.can_manage(interaction, "moderator"):
            await interaction.response.send_message("❌ Tu n'as pas la permission.", ephemeral=True)
            return

        try:
            await user.send(message)
        except Exception as e:
            await interaction.response.send_message(f"❌ Impossible d'envoyer le MP : {e}", ephemeral=True)
            return

        embed = discord.Embed(
            title="Message privé envoyé",
            description=f"MP envoyé à {user.mention}.",
            color=discord.Color.blue()
        )
        await interaction.response.send_message(embed=embed)

        log_event(interaction.guild, "PM", f"{interaction.user.mention} a envoyé un MP à {user.mention}.")

async def setup(bot):
    await bot.add_cog(Announce(bot))
