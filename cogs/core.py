import discord
from discord.ext import commands
from discord import app_commands

OWNER_IDS = {
    123456789012345678,
    987654321098765432,
}

class Core(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="help", description="Affiche l'aide du bot")
    async def help_cmd(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="Aide du bot",
            description="Voici les commandes principales.",
            color=discord.Color.green()
        )

        embed.add_field(
            name="🏠 Général",
            value="""
            `/help` ・『 Affiche les commandes 』
            `/list-dev` ・『 Liste des développeurs 』
            """,
            inline=False
        )

        embed.add_field(
            name="🔐 Permissions",
            value="""
            `/key` ・『 Donne une permission 』 『 Utilisateur 』『 Niveau 』
            `/unkey` ・『 Retire une permission 』 『 Utilisateur 』
            `/list-perm` ・『 Liste des permissions 』
            """,
            inline=False
        )

        embed.add_field(
            name="🛡 Modération",
            value="""
            `/warn` ・『 Avertir un membre 』 『 Utilisateur 』『 Raison 』
            `/kick` ・『 Expulser un membre 』 『 Utilisateur 』『 Raison 』
            `/ban` ・『 Bannir un membre 』 『 Utilisateur 』『 Raison 』
            `/unwarn` ・『 Retirer les warns 』 『 Utilisateur 』
            `/unban` ・『 Débannir 』 『 Utilisateur ID 』
            `/bl` ・『 Blacklist 』 『 Utilisateur 』『 Raison 』
            `/unbl` ・『 Retirer la blacklist 』 『 Utilisateur 』
            `/list-warn` ・『 Liste des warns 』
            `/list-ban` ・『 Liste des bans 』
            `/list-bl` ・『 Liste blacklist 』
            """,
            inline=False
        )

        embed.add_field(
            name="🚨 Sécurité",
            value="""
            `/raid` ・『 Active ou désactive le raid 』 『 État 』
            `/anty-spam` ・『 Anti-spam 』 『 État 』
            `/logs` ・『 Définit le salon des logs 』 『 Salon 』
            """,
            inline=False
        )

        embed.add_field(
            name="📢 Annonces",
            value="""
            `/announce` ・『 Envoie une annonce 』 『 Salon 』『 Message 』
            `/pm` ・『 MP à un membre 』 『 Utilisateur 』『 Message 』
            """,
            inline=False
        )

        embed.set_footer(text="Bot Discord — base modulaire")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="list-dev", description="Affiche les développeurs du bot")
    async def list_dev(self, interaction: discord.Interaction):
        if interaction.user.id not in OWNER_IDS:
            await interaction.response.send_message("❌ Tu n'as pas accès.", ephemeral=True)
            return

        devs = []
        for uid in sorted(OWNER_IDS):
            user = interaction.guild.get_member(uid)
            if user:
                devs.append(f"- {user.mention}")
            else:
                devs.append(f"- <@{uid}>")

        embed = discord.Embed(
            title="Développeurs",
            description="\n".join(devs) if devs else "Aucun développeur enregistré.",
            color=discord.Color.orange()
        )
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Core(bot))
