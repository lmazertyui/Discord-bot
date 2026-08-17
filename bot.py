import discord
from discord.ext import commands
import os

# ⚙️ Configuration des intents (permissions que le bot demande à Discord)
intents = discord.Intents.default()
intents.message_content = True  # nécessaire pour lire le contenu des messages
intents.members = True          # nécessaire pour les events comme "un membre rejoint"

bot = commands.Bot(command_prefix="!", intents=intents)

SETUP_MARKER = "🏠・ACCUEIL"  # nom de catégorie utilisé pour détecter si le setup a déjà été fait

STRUCTURE = {
    "🏠・ACCUEIL": {
        "private_staff": False,
        "channels": ["👋・bienvenue", "📜・règlement", "📢・annonces", "ℹ️・informations", "🎭・rôles", "🔗・server-invite"],
    },
    "💬・COMMUNAUTÉ": {
        "private_staff": False,
        "channels": ["💬・chat", "🎉・media", "📸・showcase", "🎮・gaming", "🤖・bots", "🔎・finder"],
    },
    "🎁・ÉVÉNEMENTS": {
        "private_staff": False,
        "channels": ["🎉・events", "🎁・giveaways", "🏆・concours", "💎・boosters"],
    },
    "🛠️・SUPPORT": {
        "private_staff": False,
        "channels": ["🎫・support", "❓・aide", "🐛・report-bug", "🚨・report", "💡・suggestions"],
    },
    "🔐・STAFF": {
        "private_staff": True,
        "channels": ["👑・staff-chat", "📋・staff-logs", "⚠️・sanctions", "🔨・modération", "📊・logs"],
    },
}

REGLEMENT_TEXTE = (
    "🤝 Respect de tous\n"
    "🚫 Pas d'insultes/provocations\n"
    "📵 Pas de spam/flood\n"
    "🔗 Pas de liens suspects\n"
    "📢 Pas de publicité sans autorisation\n"
    "🔞 Pas de contenu NSFW\n"
    "🕵️ Pas de doxxing ou partage d'informations personnelles\n"
    "🤖 Pas d'abus des bots\n"
    "⚖️ Respect des décisions du staff\n"
    "🚨 Utiliser les tickets pour signaler un problème"
)


async def creer_structure_serveur(guild: discord.Guild):
    """Crée les catégories, salons et publie le règlement. Exécuté une seule fois."""
    print(f"🏗️ Setup en cours pour le serveur : {guild.name}")

    everyone_role = guild.default_role

    for nom_categorie, infos in STRUCTURE.items():
        overwrites = {}
        if infos["private_staff"]:
            # catégorie STAFF : invisible pour @everyone
            overwrites = {
                everyone_role: discord.PermissionOverwrite(view_channel=False),
                guild.me: discord.PermissionOverwrite(view_channel=True, send_messages=True),
            }
            for role in guild.roles:
                if role.permissions.administrator:
                    overwrites[role] = discord.PermissionOverwrite(view_channel=True)

        categorie = await guild.create_category(name=nom_categorie, overwrites=overwrites)
        print(f"📁 Catégorie créée : {nom_categorie}")

        for nom_salon in infos["channels"]:
            salon = await categorie.create_text_channel(name=nom_salon)
            print(f"   └─ Salon créé : {nom_salon}")

            if nom_salon == "📜・règlement":
                embed = discord.Embed(
                    title="📜・RÈGLEMENT — SYRO COMMUNITY",
                    description=REGLEMENT_TEXTE,
                    color=discord.Color.blurple(),
                )
                await salon.send(embed=embed)
                print("      📜 Règlement publié")

    print("💾 Setup terminé pour ce serveur.")


@bot.event
async def on_ready():
    print(f"✅ Connecté en tant que {bot.user} (ID: {bot.user.id})")

    for guild in bot.guilds:
        # Vérifie si la catégorie marqueur existe déjà -> setup déjà fait
        deja_fait = discord.utils.get(guild.categories, name=SETUP_MARKER)
        if deja_fait:
            print(f"⏭️ Setup déjà effectué pour {guild.name}, on ne touche à rien.")
            continue
        try:
            await creer_structure_serveur(guild)
        except discord.Forbidden:
            print(f"❌ Permissions insuffisantes pour créer la structure sur {guild.name}")
        except Exception as e:
            print(f"❌ Erreur pendant le setup sur {guild.name} : {e}")

    print("🟢 Le bot est prêt et en ligne.")

@bot.command()
async def ping(ctx):
    """Vérifie la latence du bot"""
    latence = round(bot.latency * 1000)
    await ctx.send(f"🏓 Pong ! Latence : {latence}ms")

@bot.command()
async def bonjour(ctx):
    """Le bot dit bonjour"""
    await ctx.send(f"Salut {ctx.author.mention} 👋")

# 🔑 Le token est lu depuis une variable d'environnement (jamais écrit en dur ici)
token = os.getenv("DISCORD_TOKEN")

if token is None:
    print("❌ Erreur : le token n'est pas défini. Ajoute la variable DISCORD_TOKEN sur Railway.")
else:
    bot.run(token)
