import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import glob
import asyncio
from core.logs import get_logger

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
    folders = ["cogs", "core", "utils"]
    ignore_modules = ["core.database","core.logs"]

    for folder in folders:
        if folder in ["__pycache__", "venv", "logs"]:
            logger.info(f"Ignoring the folder: {folder}")
            continue

        for path in glob.glob(f"{folder}/**/*.py", recursive=True):
            module_path = os.path.splitext(path)[0]
            module_path = module_path.replace("/", ".").replace("\\", ".")

            if module_path in ignore_modules:
                continue

            if "__init__" in module_path or module_path.startswith("._"):
                logger.info(f"Ignoring file: {module_path}")
                continue

            logger.info(f"Loading: {module_path}")
            try:
                await bot.load_extension(module_path)
                logger.info(f"Script {module_path} loaded!")  # Log quando a cog for carregada com sucesso
            except commands.ExtensionAlreadyLoaded:
                pass
            except Exception as e:
                logger.error(f"Couldn't load cog {module_path}: {e}")  # Log do erro ao carregar a cog

async def main():
    logger.info("Bot is starting...")  # Log quando o bot começa a iniciar
    logger.info("Loading database...")
    await bot.load_extension("core.database")
    logger.info("Database loaded!")
    logger.info("Loading other cogs...")
    await load_extensions()  # Carregar as cogs antes de iniciar o bot
    try:
        await bot.start(DISCORD_TOKEN)  # Iniciar o bot
    except Exception as e:
        logger.critical(f"Failed to start bot: {e}")  # Log de erro crítico se o bot não iniciar

# Iniciar o bot
asyncio.run(main())