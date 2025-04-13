
import discord
from discord.ext import commands
from discord import app_commands
from keep_alive import keep_alive
import os

TOKEN = os.environ.get("DISCORD_BOT_TOKEN")
GUILD_ID = 1200797806940659752
ADMIN_CHANNEL_ID = 1200802706156158996
ADMIN_ID = 1351933535627378719
ROLE_ID = 1360969155708190771

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)
tree = bot.tree

class ApproveView(discord.ui.View):
    def __init__(self, user: discord.Member):
        super().__init__(timeout=None)
        self.user = user

    @discord.ui.button(label="✅ Approve", style=discord.ButtonStyle.success)
    async def approve(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != ADMIN_ID:
            return await interaction.response.send_message("❌ มึงไม่ใช่แอดมิน", ephemeral=True)
        role = interaction.guild.get_role(ROLE_ID)
        if role is None:
            return await interaction.response.send_message(f"❌ ไม่พบยศ", ephemeral=True)
        try:
            await self.user.add_roles(role)
            await interaction.response.send_message(f"✅ เพิ่มยศให้ {self.user.mention} แล้ว")
        except discord.Forbidden:
            await interaction.response.send_message("🚫 บอทไม่มีสิทธิ์ให้ยศ", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"❌ Error: {str(e)}", ephemeral=True)

    @discord.ui.button(label="❌ Reject", style=discord.ButtonStyle.danger)
    async def reject(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != ADMIN_ID:
            return await interaction.response.send_message("❌ มึงไม่ใช่แอดมิน", ephemeral=True)
        try:
            await self.user.send(
                "❌ คำตอบของมึงยังไม่ผ่าน ลองใหม่ด้วย `/grooming`

"
                "📌 ตอบให้ดูจริงใจหน่อยนะเว้ย 😎"
            )
            await interaction.response.send_message(f"📨 แจ้ง {self.user.mention} แล้ว", ephemeral=True)
        except discord.Forbidden:
            await interaction.response.send_message("⚠️ ส่ง DM ไม่ได้", ephemeral=True)

class GroomingModal(discord.ui.Modal, title="📛 สมัครยศ Kai Grooming Fc"):
    answer = discord.ui.TextInput(
        label="มึงรู้จัก Kai Grooming ได้ยังไง?",
        style=discord.TextStyle.paragraph,
        required=True,
        max_length=500
    )
    def __init__(self, user):
        super().__init__()
        self.user = user
    async def on_submit(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="✂️ คำตอบจากผู้ใช้",
            description=f"**จาก:** {self.user.mention}

```{self.answer.value}```",
            color=discord.Color.orange()
        )
        view = ApproveView(self.user)
        channel = bot.get_channel(ADMIN_CHANNEL_ID)
        if not channel:
            return await interaction.response.send_message("❌ ไม่เจอห้องแอดมิน", ephemeral=True)
        await channel.send(embed=embed, view=view)
        await interaction.response.send_message("📨 ส่งคำตอบให้แอดมินแล้ว", ephemeral=True)

class FormButtonView(discord.ui.View):
    def __init__(self, user):
        super().__init__(timeout=None)
        self.user = user
    @discord.ui.button(label="📝 กรอกฟอร์มสมัครยศ", style=discord.ButtonStyle.primary)
    async def open_form(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.user.id:
            return await interaction.response.send_message("❌ มึงไม่ใช่เจ้าของปุ่มนี้", ephemeral=True)
        await interaction.response.send_modal(GroomingModal(self.user))

@tree.command(name="grooming", description="สมัครยศ Kai Grooming Fc", guild=discord.Object(id=GUILD_ID))
async def grooming(interaction: discord.Interaction):
    embed = discord.Embed(
        title="📛 สมัครยศ Kai Grooming Fc",
        description="กดปุ่มด้านล่างเพื่อกรอกฟอร์มสมัคร Kai Grooming Fc",
        color=discord.Color.blue()
    )
    await interaction.response.send_message(embed=embed, view=FormButtonView(interaction.user), ephemeral=True)

@bot.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=GUILD_ID))
    print(f"✅ Bot พร้อมแล้ว: {bot.user}")

keep_alive()
bot.run(TOKEN)
