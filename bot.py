import os
import discord
from discord import app_commands
from discord.ext import commands

# ============================================================
# CONFIGURATION
# ============================================================
TOKEN = os.getenv("DISCORD_TOKEN")  # Mets ton token dans une variable d'environnement sur Railway

intents = discord.Intents.default()
intents.members = True  # Nécessaire pour que le bot voie correctement les rôles et permissions des membres
bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"Connecté en tant que {bot.user} (ID: {bot.user.id})")
    try:
        synced = await bot.tree.sync()
        print(f"{len(synced)} commande(s) slash synchronisée(s).")
    except Exception as e:
        print(f"Erreur de synchronisation des commandes : {e}")


# ============================================================
# COMMANDE /upload
# ============================================================
@bot.tree.command(name="upload", description="Publish a polished script showcase post.")
@app_commands.describe(
    title="The title or name of the post.",
    loadstring="The script loadstring to showcase.",
    image_url="Optional: a direct link to an image.",
    image="Optional: an image uploaded from your gallery/files.",
)
@app_commands.default_permissions(administrator=True)
async def upload(
    interaction: discord.Interaction,
    title: str,
    loadstring: str,
    image_url: str = None,
    image: discord.Attachment = None,
):
    # Double vérification : seuls les administrateurs peuvent utiliser cette commande
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message(
            "⛔ Seuls les administrateurs du serveur peuvent utiliser cette commande.",
            ephemeral=True,
        )
        return

    # On protège le code contre les balises Discord qui casseraient le bloc de code
    safe_loadstring = loadstring.replace("```", "``\u200b`")

    embed = discord.Embed(
        title=title,
        description=f"```lua\n{safe_loadstring}\n```",
        color=discord.Color.blurple(),
    )
    embed.set_footer(
        text=f"Publié par {interaction.user.display_name}",
        icon_url=interaction.user.display_avatar.url,
    )

    # Priorité à l'image uploadée si les deux sont fournies
    if image is not None:
        if not image.content_type or not image.content_type.startswith("image/"):
            await interaction.response.send_message(
                "⚠️ Le fichier fourni dans `image` n'est pas une image valide.",
                ephemeral=True,
            )
            return
        embed.set_image(url=image.url)
    elif image_url:
        embed.set_image(url=image_url)

    await interaction.response.send_message(embed=embed)


@bot.tree.command(name="debugperms", description="Debug: affiche tes permissions telles que le bot les voit.")
async def debugperms(interaction: discord.Interaction):
    if interaction.guild is None:
        await interaction.response.send_message("Cette commande doit être utilisée dans un serveur.", ephemeral=True)
        return

    member = interaction.user
    lines = [
        f"Utilisateur : {member} (ID: {member.id})",
        f"Rôles : {', '.join(r.name for r in member.roles)}",
        f"guild_permissions.administrator : {member.guild_permissions.administrator}",
        f"Est propriétaire du serveur : {interaction.guild.owner_id == member.id}",
        f"interaction.permissions.administrator (contexte salon) : {interaction.permissions.administrator}",
    ]
    await interaction.response.send_message("```\n" + "\n".join(lines) + "\n```", ephemeral=True)


bot.run(TOKEN)
