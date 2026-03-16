import os
import logging
from contextlib import contextmanager

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)


def get_connection_string() -> str:
    """Monta a connection string a partir das variáveis de ambiente."""
    required = ["DB_USER", "DB_PASSWORD", "DB_HOST", "DB_PORT", "DB_NAME"]
    missing = [var for var in required if not os.getenv(var)]
    
    if missing:
        raise EnvironmentError(f"Variáveis de ambiente ausentes: {', '.join(missing)}")

    return (
        f"postgresql+psycopg2://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
        f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    )


@contextmanager
def get_engine():
    """Context manager para criação e descarte seguro do engine."""
    engine = create_engine(
        get_connection_string(),
        pool_pre_ping=True,      # valida conexão antes de usar
        pool_size=5,
        max_overflow=10,
        connect_args={"connect_timeout": 10}
    )
    try:
        yield engine
    finally:
        engine.dispose()