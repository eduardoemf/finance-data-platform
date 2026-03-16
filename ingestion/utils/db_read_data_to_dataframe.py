import logging

import pandas as pd
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from ingestion.utils.db_engine import get_engine

logger = logging.getLogger(__name__)


def read_sql_to_dataframe(
    query: str,
    params: dict | None = None,
    chunksize: int | None = None,
    verbose: bool = False
) -> pd.DataFrame:
    if not query or not query.strip():
        raise ValueError("A query não pode ser vazia.")

    if verbose:
        logger.info(f"Executando query: {query[:120]}{'...' if len(query) > 120 else ''}")

    with get_engine() as engine:
        try:
            with engine.connect() as conn:
                if chunksize:
                    chunks = pd.read_sql_query(
                        sql=text(query),
                        con=conn,
                        params=params,
                        chunksize=chunksize,
                    )
                    df = pd.concat(chunks, ignore_index=True)
                else:
                    df = pd.read_sql_query(
                        sql=text(query),
                        con=conn,
                        params=params,
                    )

            if verbose:
                logger.info(f"Query retornou {len(df)} linhas e {len(df.columns)} colunas.")
            
            return df

        except SQLAlchemyError as e:
            logger.error(f"Erro ao executar query: {e}")
            raise
