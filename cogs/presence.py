import discord
from discord.ext import commands

class Presence(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        # Bot Presence with streaming
        await self.bot.change_presence(
            activity=discord.Game(name=".gg/NoLife | Powered by NoLife Dev Team")
        )

async def setup(bot):
    await bot.add_cog(Presence(bot))  

