import logging

import pandas as pd
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from ingestion.utils.db_engine import get_engine

logger = logging.getLogger(__name__)


def ensure_schema(engine, schema: str) -> None:
    """Cria o schema no banco se ainda não existir."""
    with engine.connect() as conn:
        conn.execute(text(f'CREATE SCHEMA IF NOT EXISTS "{schema}"'))
        conn.commit()
        logger.info(f"Schema '{schema}' verificado/criado.")


def ingest_dataframe(
    df: pd.DataFrame,
    table_name: str,
    schema: str = "raw",
    chunksize: int = 1000,
    if_exists: str = "append",
) -> None:
    if df.empty:
        logger.warning("DataFrame vazio recebido. Nenhum dado inserido.")
        return

    if if_exists not in ("append", "replace"):
        raise ValueError(f"Valor inválido para if_exists: '{if_exists}'. Use 'append' ou 'replace'.")

    total_rows = len(df)
    logger.info(f"Iniciando ingestão: {total_rows} linhas → {schema}.{table_name}")

    with get_engine() as engine:
        ensure_schema(engine, schema)

        try:
            df.to_sql(
                name=table_name,
                schema=schema,
                con=engine,
                if_exists=if_exists,
                index=False,
                chunksize=chunksize,
                method="multi",
            )
            logger.info(f"Ingestão concluída: {total_rows} linhas inseridas em '{schema}.{table_name}'.")

        except SQLAlchemyError as e:
            logger.error(f"Erro durante a ingestão em '{schema}.{table_name}': {e}")
            raise