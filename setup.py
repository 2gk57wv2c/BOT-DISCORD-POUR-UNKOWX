#!/usr/bin/env python3
"""Configuration interactif pour SITE-453 Discord Bot.

Crée le fichier .env avec les paramètres essentiels du bot.
"""

import os
import sys
from pathlib import Path


def clear():
    os.system("cls" if os.name == "nt" else "clear")


def print_banner():
    print(
        """
╔════════════════════════════════════════════════════════════╗
║          🚨 SITE-453 SETUP - Configuration 🚨             ║
║            SCP:RP Discord Bot - Setup Wizard               ║
╚════════════════════════════════════════════════════════════╝
        """
    )


def get_input(prompt: str, default: str = "") -> str:
    """Demande une entrée utilisateur avec une valeur par défaut optionnelle."""
    if default:
        user_input = input(f"{prompt} [{default}]: ").strip()
        return user_input if user_input else default
    while True:
        user_input = input(f"{prompt}: ").strip()
        if user_input:
            return user_input
        print("❌ Cette valeur est requise.")


def get_discord_id(prompt: str) -> str:
    """Demande un ID Discord valide."""
    while True:
        user_id = input(f"{prompt}: ").strip()
        if user_id == "":
            return ""
        if user_id.isdigit() and len(user_id) >= 17:
            return user_id
        print("❌ L'ID Discord doit être un nombre valide (17+ chiffres) ou laisser vide.")


def get_yes_no(prompt: str, default: bool = True) -> bool:
    """Demande une confirmation oui/non."""
    default_str = "o/n" if default else "n/o"
    while True:
        response = input(f"{prompt} [{default_str}]: ").strip().lower()
        if response == "":
            return default
        if response in {"o", "oui", "y", "yes"}:
            return True
        if response in {"n", "non", "n"}:
            return False
        print("❌ Répondez par 'o' ou 'n'.")


def setup():
    clear()
    print_banner()

    env_file = Path(__file__).resolve().parent / ".env"

    print("\n" + "="*60)
    print("CONFIGURATION INITIALE DE SITE-453")
    print("="*60)

    if env_file.exists():
        print(f"\n⚠️  Le fichier .env existe déjà : {env_file}")
        if not get_yes_no("Voulez-vous le reconfigurer ?", default=False):
            print("❌ Configuration annulée.")
            return
        print("Reconfiguration en cours...\n")
    else:
        print(f"\nCréation d'un nouveau fichier .env : {env_file}\n")

    # Token Discord (obligatoire)
    print("\n🔐 AUTHENTIFICATION DISCORD")
    print("-" * 60)
    print(
        "1. Allez sur https://discord.com/developers/applications\n"
        "2. Créez une nouvelle application\n"
        "3. Allez dans l'onglet 'Bot' et cliquez sur 'Add Bot'\n"
        "4. Copiez le token sous 'TOKEN'"
    )
    token = get_input("\nPaste le token Discord du bot")

    # IDs du Commandant (propriétaire)
    print("\n👤 IDENTIFIANTS DES PROPRIÉTAIRES")
    print("-" * 60)
    print(
        "Pour obtenir un ID Discord :\n"
        "1. Activez le Mode Développeur (Paramètres > Avancés > Mode Développeur)\n"
        "2. Clic droit sur un utilisateur > Copier l'ID utilisateur"
    )
    owner_id = get_discord_id("\nID du Commandant SITE-453 (propriétaire principal)")
    if not owner_id:
        print("❌ Un propriétaire est requis pour le bot.")
        return

    co_owners = get_input(
        "\nIDs des Co-Commandants (séparés par des virgules, ou laisser vide)",
        default="",
    )

    # Préfixe du bot
    print("\n⚙️  CONFIGURATION GÉNÉRALE")
    print("-" * 60)
    prefix = get_input("Préfixe des commandes texte", default="!")
    if prefix == "/":
        print("⚠️  Le préfixe '/' entre en conflit avec les slash commands.")
        prefix = "!"

    # Statut du bot
    activity = get_input(
        "Statut/Activité du bot",
        default="SITE-453 — FALL FROM THE SKY",
    )

    # Serveur de test (optionnel)
    print("\n🧪 CONFIGURATION DE TEST (OPTIONNEL)")
    print("-" * 60)
    guild_id = get_input(
        "ID du serveur de test (pour sync instant des slash commands, ou laisser vide)",
        default="",
    )

    # Salon des logs (optionnel)
    log_channel = get_input(
        "ID du salon des logs (ou laisser vide pour plus tard)",
        default="",
    )

    # Features (optionnel)
    print("\n🎮 FONCTIONNALITÉS")
    print("-" * 60)
    enable_tickets = get_yes_no("Activer les tickets ?", default=True)
    enable_logs = get_yes_no("Activer les logs de modération ?", default=True)
    enable_music = get_yes_no("Activer la musique ? (bêta)", default=False)
    enable_members = get_yes_no(
        "Activer l'intent Members ? (requis pour certaines fonctions)",
        default=True,
    )
    enable_message_content = get_yes_no(
        "Activer l'intent Message Content ? (requis pour les commandes texte)",
        default=True,
    )

    # Crédits
    dev_credits = get_input(
        "Crédits développeur",
        default="nathanre0100 — fondateur SITE-453",
    )

    # Construction du fichier .env
    print("\n" + "="*60)
    print("GÉNÉRATION DU FICHIER .env")
    print("="*60 + "\n")

    env_content = f"""# Discord Bot Configuration - SITE-453
# Configuration générée par setup.py

# ==== AUTHENTIFICATION ====
DISCORD_TOKEN={token}
BOT_PREFIX={prefix}

# ==== PROPRIÉTAIRES ====
BOT_OWNER_ID={owner_id}
CO_OWNER_IDS={co_owners}
GLOBAL_ADMIN_IDS=

# ==== CONFIGURATION SERVEUR ====
GUILD_ID={guild_id}
LOG_CHANNEL_ID={log_channel}
BOT_ACTIVITY={activity}

# ==== OPTIONNEL ====
SUPPORT_SERVER=
DASHBOARD_URL=
DEV_CREDITS={dev_credits}
NEXUS_SECRET=
NEXUS_PORT=8765

# ==== BASE DE DONNÉES ====
DATABASE_URL=sqlite:///./data/database.db

# ==== FONCTIONNALITÉS ====
ENABLE_MUSIC={'true' if enable_music else 'false'}
ENABLE_TICKETS={'true' if enable_tickets else 'false'}
ENABLE_LOGS={'true' if enable_logs else 'false'}
ENABLE_MESSAGE_CONTENT={'true' if enable_message_content else 'false'}
ENABLE_MEMBERS={'true' if enable_members else 'false'}
"""

    try:
        env_file.write_text(env_content, encoding="utf-8")
        print(f"✅ Fichier .env créé avec succès : {env_file}")
    except OSError as exc:
        print(f"❌ Erreur lors de la création du fichier : {exc}")
        return

    print("\n" + "="*60)
    print("✅ CONFIGURATION TERMINÉE")
    print("="*60)
    print(
        f"""
 Propriétaire : <@{owner_id}>
 Préfixe : {prefix}
 Statut : {activity}
 Tickets : {'✅ Activés' if enable_tickets else '❌ Désactivés'}
 Logs : {'✅ Activés' if enable_logs else '❌ Désactivés'}

Prochaines étapes :
 1. Allez sur https://discord.com/developers/applications
 2. Sélectionnez votre application
 3. Onglet 'Bot' → 'Privileged Gateway Intents'
    - Activez 'Server Members Intent'
    - Activez 'Message Content Intent'
 4. Onglet 'OAuth2' → 'URL Generator'
    - Scope : bot + applications.commands
    - Permissions : Administrator (8)
    - Ouvrez l'URL générée et invitez le bot sur votre serveur
 5. Lancez le bot avec 'python launcher.py' ou 'python main.py'

💡 Conseil : Remplacez BOT_OWNER_ID par votre ID et redémarrez le bot.
    """
    )

    input("\n[Appuyez sur Entrée pour terminer...]")


if __name__ == "__main__":
    try:
        setup()
    except KeyboardInterrupt:
        print("\n\n⏹️  Setup interrompu par l'utilisateur.")
        sys.exit(0)
