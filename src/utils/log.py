# Imports de pacotes built-in
import logging
import functools
from typing import Callable

# Imports de pacotes de terceiros
from googleapiclient.http import MediaIoBaseUpload
import io
import streamlit as st

# Se rodar localemnte
logging.basicConfig(
    filename='logs/logs_etl.log',
    filemode='a',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    encoding='utf-8'
)

log_buffer = io.StringIO()
logger = logging.getLogger(name='etl_logger')
logger.setLevel(logging.INFO)

# Handler em memória
handler = logging.StreamHandler(log_buffer)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)


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


def get_log_contents() -> str:
    return log_buffer.getvalue()


def clear_log():
    log_buffer.truncate(0)
    log_buffer.seek(0)