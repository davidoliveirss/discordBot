import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import glob
import asyncio
import logging
from logs import get_logger

logger = get_logger()

intents = discord.Intents.default()
intents.message_content = True  # Certifique-se de que esta linha está presente
intents.presences = True

# Inicializa o bot com os intents
bot = commands.Bot(command_prefix="!", intents=intents)

# Carregar o token do .env
load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

async def load_extensions():
    for cog in glob.glob("cogs/*.py"):
        extension = cog.replace("/", ".").replace(".py", "")
        if extension == "cogs.database":
            continue 
        try:
            # Remover o caminho e a extensão ".py" do nome do arquivo para usar no método load_extension
            await bot.load_extension(cog.replace("/", ".").replace(".py", ""))
            logging.info(f"Cog {cog} loaded!")  # Log quando a cog for carregada com sucesso
        except Exception as e:
            logging.error(f"Couldn't load cog {cog}: {e}")  # Log do erro ao carregar a cog

async def main():
    logging.info("Bot is starting...")  # Log quando o bot começa a iniciar
    logging.info("Starting database...")
    await bot.load_extension("cogs.database")
    logging.info("Database loaded!")
    logging.info("Starting other cogs...")
    await load_extensions()  # Carregar as cogs antes de iniciar o bot
    try:
        await bot.start(DISCORD_TOKEN)  # Iniciar o bot
    except Exception as e:
        logging.critical(f"Failed to start bot: {e}")  # Log de erro crítico se o bot não iniciar

# Iniciar o bot
asyncio.run(main())

