import discord
import random
from discord import ui 
from discord.ext import commands
from discord.ui import View, Button
from datetime import datetime, timedelta
from logs import get_logger
import os

logger = get_logger()

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.wait_until_ready()  # Aguarda até o bot estar pronto
        logger.info(f'{self.bot.user} ({self.bot.user.id}) Status: online')

async def setup(bot):
    await bot.add_cog(Events(bot))

