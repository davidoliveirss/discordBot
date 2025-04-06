from discord.ext import commands
import os
from core.logs import get_logger

logger = get_logger()

class Encrypt(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

async def setup(bot):
    await bot.add_cog(Encrypt(bot))
