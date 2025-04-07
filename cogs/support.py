import discord
from discord import ui
from discord.ext import commands
from discord.ui import View, Button
from core.logs import get_logger

logger = get_logger()

class Support(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


async def setup(bot):
    await bot.add_cog(Support(bot))