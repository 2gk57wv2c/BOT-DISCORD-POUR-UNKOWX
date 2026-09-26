# SITE-453 Discord Bot — SCP:RP

> **Bot SITE-453** — *FALL FROM THE SKY*

Bot Discord avancé pour serveurs SCP:RP avec modération, gestion des permissions et logs.

## 📋 Démarrage rapide

```bash
# 1. Cloner ou télécharger le projet
git clone <repo-url>
cd BOT-DISCORD-POUR-UNKOWX

# 2. Créer un environnement virtuel
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\\Scripts\\activate     # Windows

# 3. Installer les dépendances
pip install -r requirements.txt

# 4. Configuration initiale
python setup.py

# 5. Lancer le bot
python main.py
# Ou utiliser le launcher interactif
python launcher.py
```

## 🚀 Features

- **Modération** : warn, kick, ban, blacklist
- **Permissions** : hiérarchie de rôles (founder, cofounder, admin, moderator, member)
- **Sécurité** : mode raid, anti-spam, logs
- **Annonces** : broadcast dans les salons, MPs personnalisés
- **Launcher** : interface graphique pour gérer le bot (local/Raspberry Pi)

## 🔐 Configuration

Copie `.env.example` en `.env` et configure :

```env
DISCORD_TOKEN=ton_token_ici
BOT_OWNER_ID=ton_id_discord
BOT_PREFIX=!
```

Ou utilise le setup interactif :

```bash
python setup.py
```

## 📖 Commandes principales

| Commande | Description |
|----------|-------------|
| `/help` | Affiche l'aide |
| `/key @user level` | Donne une permission |
| `/warn @user reason` | Avertit un utilisateur |
| `/kick @user reason` | Expulse un utilisateur |
| `/ban @user reason` | Bannit un utilisateur |
| `/logs #channel` | Définit le salon des logs |
| `/raid on/off` | Active/désactive le mode raid |
| `/announce #channel message` | Envoie une annonce |

## 🍓 Raspberry Pi

Le launcher supporte le lancement à distance via SSH :

```bash
python launcher.py
# Option 11 : Configurer Raspberry Pi
```

Prérequis :
- SSH activé sur le Pi
- Clé SSH configurée (sans mot de passe)
- SITE-453 copié sur le Pi

## 📝 Développement

Structure du projet :

```
.
├── main.py              # Point d'entrée principal
├── config.py            # Configuration centralisée
├── setup.py             # Configuration interactif
├── launcher.py          # Launcher avec interface
├── requirements.txt      # Dépendances Python
├── utils/
│   └── db.py            # Helpers base de données
├── cogs/                # Modules de commandes
│   ├── core.py
│   ├── permissions.py
│   ├── moderation.py
│   ├── security.py
│   └── announce.py
└── data/                # Données persistantes (créé automatiquement)
    └── database.db      # SQLite
```

## 🔗 Liens utiles

- [Discord Developer Portal](https://discord.com/developers/applications)
- [discord.py Documentation](https://discordpy.readthedocs.io/)
- [SCP Foundation](https://scp-wiki.wikidot.com/)

## 📄 Licence

Projet privé — Nathan RE0100 — Fondateur SITE-453

---

**SITE-453** — *FALL FROM THE SKY* 🚨
