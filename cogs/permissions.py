import discord
from discord.ext import commands
from discord import app_commands

from utils.db import get_all_permissions, set_user_level, remove_user_level, user_has_at_least, log_event

OWNER_IDS = {
    123456789012345678,
    987654321098765432,
}


class Permissions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def can_manage(self, interaction: discord.Interaction, required: str = "admin"):
        if interaction.user.id in OWNER_IDS:
            return True
        return user_has_at_least(interaction.guild.id, interaction.user.id, required, owner_ids=OWNER_IDS)

    @app_commands.command(name="key", description="Donne une permission à un membre")
    @app_commands.describe(user="Utilisateur", level="Niveau de permission", reason="Raison")
    async def key_cmd(self, interaction: discord.Interaction, user: discord.Member, level: str, reason: str = "Aucune raison"):
        if interaction.user.id not in OWNER_IDS:
            await interaction.response.send_message("❌ Seul le fondateur peut attribuer des permissions.", ephemeral=True)
            return

        valid_levels = {"founder", "cofounder", "admin", "moderator", "member"}
        if level not in valid_levels:
            await interaction.response.send_message(
                "❌ Niveau invalide. Valeurs acceptées : founder, cofounder, admin, moderator, member",
                ephemeral=True,
            )
            return

        set_user_level(interaction.guild.id, user.id, level, reason, interaction.user.id)

        embed = discord.Embed(
            title="Permission attribuée",
            description=f"{user.mention} a reçu le niveau `{level}`.",
            color=discord.Color.green(),
        )
        embed.add_field(name="Raison", value=reason, inline=False)
        await interaction.response.send_message(embed=embed)

        log_event(interaction.guild, "Permission", f"{interaction.user.mention} a donné le niveau `{level}` à {user.mention}. Raison : {reason}")

    @app_commands.command(name="unkey", description="Retire une permission à un membre")
    @app_commands.describe(user="Utilisateur", reason="Raison")
    async def unkey_cmd(self, interaction: discord.Interaction, user: discord.Member, reason: str = "Aucune raison"):
        if interaction.user.id not in OWNER_IDS:
            await interaction.response.send_message("❌ Seul le fondateur peut retirer des permissions.", ephemeral=True)
            return

        remove_user_level(interaction.guild.id, user.id)

        embed = discord.Embed(
            title="Permission retirée",
            description=f"{user.mention} n'a plus de permission spéciale.",
            color=discord.Color.orange(),
        )
        embed.add_field(name="Raison", value=reason, inline=False)
        await interaction.response.send_message(embed=embed)

        log_event(interaction.guild, "Permission retirée", f"{interaction.user.mention} a retiré la permission à {user.mention}. Raison : {reason}")

    @app_commands.command(name="list-perm", description="Affiche les permissions du serveur")
    async def list_perm(self, interaction: discord.Interaction):
        if interaction.user.id not in OWNER_IDS:
            await interaction.response.send_message("❌ Tu n'as pas accès.", ephemeral=True)
            return

        rows = get_all_permissions(interaction.guild.id)
        if not rows:
            await interaction.response.send_message("Aucune permission enregistrée.", ephemeral=True)
            return

        lines = []
        for row in rows:
            member = interaction.guild.get_member(row["user_id"])
            display = member.mention if member else f"<@{row['user_id']}>"
            lines.append(f"{display} → `{row['level']}` — {row['reason']}")

        embed = discord.Embed(
            title="Permissions du serveur",
            description="\n".join(lines),
            color=discord.Color.blue(),
        )
        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(Permissions(bot))
