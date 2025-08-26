# Imports de pacotes built-in
import logging
import functools
from typing import Callable

logging.basicConfig(
    filename='logs/logs_etl.log',
    filemode='a',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    encoding='utf-8'
)

logger = logging.getLogger()

def log(func: Callable) -> Callable:
    """Decorador simples que registra execução e exceções."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            logger.info(f'{func.__name__} executada com excesso!') # Manter?
            return result
        except Exception as error:
            logger.exception(f"Erro em {func.__name__}")
            return error
    return wrapper