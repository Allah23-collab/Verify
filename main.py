
import discord
from discord.ext import commands
from discord import app_commands
from keep_alive import keep_alive
import os

# CONFIG (ใช้ ENV แทน Token)
TOKEN = os.environ.get("DISCORD_BOT_TOKEN")
GUILD_ID = 1200797806940659752
ADMIN_CHANNEL_ID = 1200802706156158996
ADMIN_ID = 1351933535627378719
ROLE_ID = 1200832835688697886

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)
tree = bot.tree

# ===== CLASS ทั้งหมดให้มึงยัดจากโค้ดก่อนหน้า (ApproveView, Modal, View, Slash Command) =====

@bot.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=GUILD_ID))
    print(f"✅ Bot พร้อมแล้ว: {bot.user}")

keep_alive()
bot.run(TOKEN)
