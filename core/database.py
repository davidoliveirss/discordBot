import mysql.connector
from mysql.connector import Error
from core.logs import get_logger
from discord.ext import commands

logger = get_logger()

class Database(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

def create_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='discord_bot',
            user='discordBot',
            password='discordBot.132'
        )
        if connection.is_connected():
            return connection
    except Error as e:
        logger.info(f"Couldn't connect to MySQL: {e}")
        return None

async def setup(bot):
    await bot.add_cog(Database(bot))
