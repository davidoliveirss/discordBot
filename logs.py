import logging

# Configurar o sistema de logs
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("logs/bot.log"),  # Salva os logs no arquivo bot.log
        logging.StreamHandler()  # Exibe os logs no terminal
    ]
)

# Obter o logger configurado
logger = logging.getLogger(__name__)

# Função para retornar o logger
def get_logger():
    return logger

