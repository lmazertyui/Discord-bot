import discord
from discord.ext import commands
import os

# ⚙️ Configuration des intents (permissions que le bot demande à Discord)
intents = discord.Intents.default()
intents.message_content = True  # nécessaire pour lire le contenu des messages
intents.members = True          # nécessaire pour les events comme "un membre rejoint"

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Connecté en tant que {bot.user} (ID: {bot.user.id})")
    print("Le bot est prêt !")

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
