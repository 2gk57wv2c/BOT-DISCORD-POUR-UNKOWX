import discord
from discord.ext import commands
from discord import app_commands

from utils.db import (
    add_ban,
    add_blacklist,
    add_kick_log,
    add_warn,
    clear_warns,
    get_bans,
    get_blacklist,
    get_warns,
    log_event,
    remove_blacklist,
    user_has_at_least,
)

OWNER_IDS = {
    123456789012345678,
    987654321098765432,
}

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def can_mod(self, interaction: discord.Interaction, required: str = "moderator"):
        if interaction.user.id in OWNER_IDS:
            return True
        return user_has_at_least(interaction.guild.id, interaction.user.id, required, owner_ids=OWNER_IDS)

    @app_commands.command(name="warn", description="Avertit un membre")
    @app_commands.describe(user="Utilisateur", reason="Raison")
    async def warn_cmd(self, interaction: discord.Interaction, user: discord.Member, reason: str = "Aucune raison"):
        if not self.can_mod(interaction, "moderator"):
            await interaction.response.send_message("❌ Tu n'as pas la permission.", ephemeral=True)
            return

        add_warn(interaction.guild.id, user.id, interaction.user.id, reason)
        warn_count = len(get_warns(interaction.guild.id, user.id))

        embed = discord.Embed(
            title="Avertissement",
            description=f"{user.mention} a reçu un avertissement.",
            color=discord.Color.yellow()
        )
        embed.add_field(name="Nombre total", value=str(warn_count), inline=False)
        embed.add_field(name="Raison", value=reason, inline=False)
        await interaction.response.send_message(embed=embed)

        log_event(interaction.guild, "Warn", f"{interaction.user.mention} a warn {user.mention}. Raison : {reason}")

    @app_commands.command(name="unwarn", description="Retire les warns d'un membre")
    @app_commands.describe(user="Utilisateur")
    async def unwarn_cmd(self, interaction: discord.Interaction, user: discord.Member):
        if not self.can_mod(interaction, "moderator"):
            await interaction.response.send_message("❌ Tu n'as pas la permission.", ephemeral=True)
            return

        clear_warns(interaction.guild.id, user.id)

        embed = discord.Embed(
            title="Warns retirés",
            description=f"Les warns de {user.mention} ont été supprimés.",
            color=discord.Color.green()
        )
        await interaction.response.send_message(embed=embed)

        log_event(interaction.guild, "Warn retiré", f"{interaction.user.mention} a retiré les warns de {user.mention}.")

    @app_commands.command(name="list-warn", description="Affiche les warns d'un membre")
    @app_commands.describe(user="Utilisateur")
    async def list_warn(self, interaction: discord.Interaction, user: discord.Member):
        if not self.can_mod(interaction, "moderator"):
            await interaction.response.send_message("❌ Tu n'as pas la permission.", ephemeral=True)
            return

        rows = get_warns(interaction.guild.id, user.id)
        if not rows:
            await interaction.response.send_message(f"{user.mention} n'a aucun warn.", ephemeral=True)
            return

        lines = []
        for row in rows:
            lines.append(f"- {row['created_at']} — {row['reason']}")

        embed = discord.Embed(
            title=f"Warns de {user.display_name}",
            description="\n".join(lines),
            color=discord.Color.gold()
        )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="kick", description="Expulse un membre")
    @app_commands.describe(user="Utilisateur", reason="Raison")
    async def kick_cmd(self, interaction: discord.Interaction, user: discord.Member, reason: str = "Aucune raison"):
        if not self.can_mod(interaction, "moderator"):
            await interaction.response.send_message("❌ Tu n'as pas la permission.", ephemeral=True)
            return

        add_kick_log(interaction.guild.id, user.id, interaction.user.id, reason)

        try:
            await user.kick(reason=reason)
        except Exception as e:
            await interaction.response.send_message(f"❌ Impossible de kicker {user.mention} : {e}", ephemeral=True)
            return

        embed = discord.Embed(
            title="Kick",
            description=f"{user.mention} a été expulsé.",
            color=discord.Color.orange()
        )
        embed.add_field(name="Raison", value=reason, inline=False)
        await interaction.response.send_message(embed=embed)

        log_event(interaction.guild, "Kick", f"{interaction.user.mention} a kick {user.mention}. Raison : {reason}")

    @app_commands.command(name="ban", description="Bannit un membre")
    @app_commands.describe(user="Utilisateur", reason="Raison")
    async def ban_cmd(self, interaction: discord.Interaction, user: discord.Member, reason: str = "Aucune raison"):
        if not self.can_mod(interaction, "moderator"):
            await interaction.response.send_message("❌ Tu n'as pas la permission.", ephemeral=True)
            return

        add_ban(interaction.guild.id, user.id, interaction.user.id, reason)

        try:
            await user.ban(reason=reason)
        except Exception as e:
            await interaction.response.send_message(f"❌ Impossible de bannir {user.mention} : {e}", ephemeral=True)
            return

        embed = discord.Embed(
            title="Ban",
            description=f"{user.mention} a été banni.",
            color=discord.Color.red()
        )
        embed.add_field(name="Raison", value=reason, inline=False)
        await interaction.response.send_message(embed=embed)

        log_event(interaction.guild, "Ban", f"{interaction.user.mention} a ban {user.mention}. Raison : {reason}")

    @app_commands.command(name="unban", description="Débannit un membre par ID")
    @app_commands.describe(user_id="ID Discord de l'utilisateur")
    async def unban_cmd(self, interaction: discord.Interaction, user_id: str):
        if not self.can_mod(interaction, "moderator"):
            await interaction.response.send_message("❌ Tu n'as pas la permission.", ephemeral=True)
            return

        try:
            user_id_int = int(user_id)
        except ValueError:
            await interaction.response.send_message("❌ L'ID est invalide.", ephemeral=True)
            return

        try:
            await interaction.guild.unban(discord.Object(id=user_id_int))
        except Exception as e:
            await interaction.response.send_message(f"❌ Impossible de débannir : {e}", ephemeral=True)
            return

        embed = discord.Embed(
            title="Unban",
            description=f"L'utilisateur <@{user_id_int}> a été débanni.",
            color=discord.Color.green()
        )
        await interaction.response.send_message(embed=embed)

        log_event(interaction.guild, "Unban", f"{interaction.user.mention} a débanni <@{user_id_int}>.")

    @app_commands.command(name="list-ban", description="Affiche les bans du serveur")
    async def list_ban(self, interaction: discord.Interaction):
        if not self.can_mod(interaction, "moderator"):
            await interaction.response.send_message("❌ Tu n'as pas la permission.", ephemeral=True)
            return

        rows = get_bans(interaction.guild.id)
        if not rows:
            await interaction.response.send_message("Aucun ban enregistré.", ephemeral=True)
            return

        lines = []
        for row in rows:
            display = f"<@{row['user_id']}>"
            lines.append(f"- {display} — {row['reason']}")

        embed = discord.Embed(
            title="Liste des bans",
            description="\n".join(lines),
            color=discord.Color.red()
        )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="bl", description="Ajoute un membre à la blacklist")
    @app_commands.describe(user="Utilisateur", reason="Raison")
    async def bl_cmd(self, interaction: discord.Interaction, user: discord.Member, reason: str = "Aucune raison"):
        if not self.can_mod(interaction, "admin"):
            await interaction.response.send_message("❌ Tu n'as pas la permission.", ephemeral=True)
            return

        add_blacklist(interaction.guild.id, user.id, interaction.user.id, reason)

        embed = discord.Embed(
            title="Blacklist",
            description=f"{user.mention} a été ajouté à la blacklist.",
            color=discord.Color.dark_red()
        )
        embed.add_field(name="Raison", value=reason, inline=False)
        await interaction.response.send_message(embed=embed)

        log_event(interaction.guild, "Blacklist", f"{interaction.user.mention} a blacklist {user.mention}. Raison : {reason}")

    @app_commands.command(name="unbl", description="Retire un membre de la blacklist")
    @app_commands.describe(user="Utilisateur")
    async def unbl_cmd(self, interaction: discord.Interaction, user: discord.Member):
        if not self.can_mod(interaction, "admin"):
            await interaction.response.send_message("❌ Tu n'as pas la permission.", ephemeral=True)
            return

        remove_blacklist(interaction.guild.id, user.id)

        embed = discord.Embed(
            title="Blacklist retirée",
            description=f"{user.mention} a été retiré de la blacklist.",
            color=discord.Color.green()
        )
        await interaction.response.send_message(embed=embed)

        log_event(interaction.guild, "Blacklist", f"{interaction.user.mention} a retiré {user.mention} de la blacklist.")

    @app_commands.command(name="list-bl", description="Affiche la blacklist du serveur")
    async def list_bl(self, interaction: discord.Interaction):
        if not self.can_mod(interaction, "admin"):
            await interaction.response.send_message("❌ Tu n'as pas la permission.", ephemeral=True)
            return

        rows = get_blacklist(interaction.guild.id)
        if not rows:
            await interaction.response.send_message("Aucune blacklist enregistrée.", ephemeral=True)
            return

        lines = []
        for row in rows:
            display = f"<@{row['user_id']}>"
            lines.append(f"- {display} — {row['reason']}")

        embed = discord.Embed(
            title="Blacklist",
            description="\n".join(lines),
            color=discord.Color.dark_red()
        )
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Moderation(bot))
