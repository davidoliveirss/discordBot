from discord.ext import commands
import os

class CustomCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.is_owner()
    async def reboot(self, ctx):
        await ctx.send("🔄 A reiniciar o bot...")
        os.system("sudo systemctl restart discord-bot.service")

async def setup(bot):
    await bot.add_cog(CustomCommands(bot))

