import discord
from discord.ext import commands
from discord import app_commands

from utils.db import update_guild_config, user_has_at_least, log_event

OWNER_IDS = {
    123456789012345678,
    987654321098765432,
}


class Security(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def can_manage(self, interaction: discord.Interaction, required: str = "admin"):
        if interaction.user.id in OWNER_IDS:
            return True
        return user_has_at_least(interaction.guild.id, interaction.user.id, required, owner_ids=OWNER_IDS)

    @app_commands.command(name="raid", description="Active ou désactive le mode raid")
    @app_commands.describe(etat="on/off")
    async def raid_cmd(self, interaction: discord.Interaction, etat: str):
        if not self.can_manage(interaction, "admin"):
            await interaction.response.send_message("❌ Tu n'as pas la permission.", ephemeral=True)
            return

        if etat.lower() not in {"on", "off"}:
            await interaction.response.send_message("❌ Utilisation : `/raid on` ou `/raid off`", ephemeral=True)
            return

        state = 1 if etat.lower() == "on" else 0
        update_guild_config(interaction.guild.id, raid=state)

        embed = discord.Embed(
            title="Mode raid",
            description=f"Le mode raid a été mis à **{etat.lower()}**.",
            color=discord.Color.orange(),
        )
        await interaction.response.send_message(embed=embed)

        log_event(interaction.guild, "Raid", f"{interaction.user.mention} a activé le mode raid : **{etat.lower()}**")

    @app_commands.command(name="anty-spam", description="Active ou désactive l'anti-spam")
    @app_commands.describe(etat="on/off")
    async def anti_spam_cmd(self, interaction: discord.Interaction, etat: str):
        if not self.can_manage(interaction, "admin"):
            await interaction.response.send_message("❌ Tu n'as pas la permission.", ephemeral=True)
            return

        if etat.lower() not in {"on", "off"}:
            await interaction.response.send_message("❌ Utilisation : `/anty-spam on` ou `/anty-spam off`", ephemeral=True)
            return

        state = 1 if etat.lower() == "on" else 0
        update_guild_config(interaction.guild.id, anti_spam=state)

        embed = discord.Embed(
            title="Anti-spam",
            description=f"L'anti-spam a été mis à **{etat.lower()}**.",
            color=discord.Color.purple(),
        )
        await interaction.response.send_message(embed=embed)

        log_event(interaction.guild, "Anti-spam", f"{interaction.user.mention} a activé l'anti-spam : **{etat.lower()}**")

    @app_commands.command(name="logs", description="Définit le salon des logs")
    @app_commands.describe(channel="Salon des logs")
    async def logs_cmd(self, interaction: discord.Interaction, channel: discord.TextChannel):
        if not self.can_manage(interaction, "admin"):
            await interaction.response.send_message("❌ Tu n'as pas la permission.", ephemeral=True)
            return

        update_guild_config(interaction.guild.id, logs_channel_id=channel.id)

        embed = discord.Embed(
            title="Logs configurés",
            description=f"Le salon {channel.mention} est maintenant utilisé pour les logs.",
            color=discord.Color.blurple(),
        )
        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(Security(bot))
