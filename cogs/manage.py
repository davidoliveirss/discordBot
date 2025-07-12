import discord
from discord import ui
from discord.ext import commands
from discord.ui import View, Button
from datetime import datetime, timedelta
from core.logs import get_logger
import os
import pwd
import socket
from collections import deque
import psutil


logger = get_logger()

class ManageView(View):
    def __init__(self):
        super().__init__(timeout=None)  # O View não expira
        self.cooldowns = {}

    @discord.ui.button(label="📴Shutdown", style=discord.ButtonStyle.danger, custom_id="shutdown")
    async def shutdown_callback(self, interaction: discord.Interaction, button: Button):
        user_id = interaction.user.id
        username = interaction.user.name
        bot_user = interaction.client.user

        logger.info(f"{bot_user} shutting down, forced by {username}({user_id}) ")
        os.system("sudo systemctl stop discord-bot.service")

    @discord.ui.button(label="🔁Reboot", style=discord.ButtonStyle.primary, custom_id="reboot")
    async def reboot_callback(self, interaction: discord.Interaction, button: Button):
        user_id = interaction.user.id
        username = interaction.user.name
        bot_user = interaction.client.user

        logger.info(f"{bot_user} rebooting, forced by {username}({user_id})")
        os.system("sudo systemctl restart discord-bot.service")

    @discord.ui.button(label="📄View logs", style=discord.ButtonStyle.secondary, custom_id="view_logs")
    async def view_logs_callback(self, interaction: discord.Interaction, button: Button):
        try:
            log_path = "/home/server/discordBot/logs/bot.log"

            with open(log_path, "r", encoding="utf-8") as f:
                lines = deque(f, maxlen=20)

            log_content = "".join(lines) if lines else "Logs file is empty."

            await interaction.response.send_message(f"```{log_content}```", ephemeral=True)

        except Exception as e:
            await interaction.response.send_message(f"Coulnt load logs: {e}", ephemeral=True)
class Manage(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.wait_until_ready()  # Aguarda até o bot estar pronto
        channel_id = 1352366039459037325
        channel = self.bot.get_channel(channel_id)

        if channel:
            await channel.purge()

            hostname = socket.gethostname()
            ip_address = socket.gethostbyname(hostname)
            host_user_name = os.getenv("USER") or pwd.getpwuid(os.getuid()).pw_name
            uptime = os.popen("uptime -p").read().strip()
            operating_system = os.uname().sysname

            guild = channel.guild
            boost_count = guild.premium_subscription_count
            boost_tier = guild.premium_tier

            cpu_usage = psutil.cpu_percent(interval=1)
            mem = psutil.virtual_memory()
            mem_usage = mem.percent

            embed = discord.Embed(
                title="Management panel",
                description="Management panel for NoLife discord bot",
                color=discord.Color.light_embed(),
            )
            embed.set_footer(text="Management system | Powered by NoLife Dev Team", icon_url="https://cdn.discordapp.com/attachments/1352771477845315685/1352791135730536548/e5b4a8673da2b6cf452368c17dad4fc5.jpg?ex=67df4c6c&is=67ddfaec&hm=14e28ef11de619bd26ba489bd5167606828c897374455e92e573c353ac00c7fa&")
            embed.add_field(name="Host infos", value=f"OS: {operating_system}\nHost name: {hostname}\nUser name: {host_user_name}\nUptime: {uptime}\nCPU usage: {cpu_usage}%\nRAM usage: {mem_usage}%\nHost ip: ||{ip_address}||", inline=True)
            embed.add_field(name="Server infos", value=f"Server name: {guild.name}\nServer id: {guild.id}\nMembers: {guild.member_count}\nBoosts: {boost_count} (Level {boost_tier})", inline=True)
            viewManage = ManageView()
            await channel.send(embed=embed, view=viewManage)
        else:
            logger.info(f"⚠️Channel not found {channel_id}!")

        @commands.Cog.listener()
        async def on_guild_update(self, before, after):
        # Verifica se o número de boosts mudou
            if before.premium_subscription_count != after.premium_subscription_count:
                if self.embed_message:
                # Atualiza o campo de boosts no embed
                    embed = self.embed_message.embeds[0]
                    embed.set_field_at(1, name="Server infos", value=f"Server name: {after.name}\nServer id: {after.id}\nMembers: {after.member_count}\nBoosts: {after.premium_subscription_count}\n Boost level: {after.premium_tier}", inline=True)
                    await self.embed_message.edit(embed=embed)  # Edita a mensagem com o novo embed

async def setup(bot):
    await bot.add_cog(Manage(bot))