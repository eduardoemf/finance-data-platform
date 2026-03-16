from typing import Any, Dict, List
from dotenv import load_dotenv
import os
import requests
import pandas as pd


def extract_api_alpha_daily(api_key: str, symbol: str = "NVDA", outputsize: str = "compact") -> pd.DataFrame:
    """
    Busca dados diários do mercado de ações a partir da API Alpha Vantage e os retorna como um DataFrame do pandas.
    Esta função consulta o endpoint TIME_SERIES_DAILY da Alpha Vantage para recuperar dados OHLCV 
    (Abertura, Máxima, Mínima, Fechamento, Volume) para um determinado ticker de ação. A resposta em JSON é 
    transformada em um DataFrame do pandas estruturado, adequado para análise posterior, armazenamento ou ingestão em pipelines de dados.

    Args:
        api_key (str): Chave de API da Alpha Vantage necessária para autenticação.
        symbol (str, opcional): Símbolo do ticker da ação a ser consultado (por exemplo, "NVDA", "AAPL", "MSFT"). O padrão é "NVDA".
        outputsize (str, opcional): Especifica a quantidade de dados históricos retornados pela API. As opções são: "compact": retorna os últimos 100 dias de negociação. "full": retorna todo o histórico disponível. O padrão é "compact".

    Returns:
        pd.DataFrame: Um DataFrame do pandas contendo os dados diários de ações no formato OHLCV, com as seguintes colunas:
            date: data de negociação
            symbol: símbolo do ticker da ação
            open: preço de abertura
            high: maior preço do dia
            low: menor preço do dia
            close: preço de fechamento
            volume: volume negociado
        O DataFrame é ordenado cronologicamente pela data.

    Raises:
        RuntimeError:
        Gerado se a requisição à API falhar ou se a estrutura de dados esperada não estiver presente na resposta da API.
    Side Effects:
        Envia uma requisição HTTP para a API da Alpha Vantage.
    """

    # DEFINE A URL BASE DA API ALPHA VANTAGE PARA CONSULTAS DE MERCADO FINANCEIRO
    ALPHA_URL = "https://www.alphavantage.co/query"

    # DEFINE OS PARÂMETROS DA REQUISIÇÃO HTTP QUE SERÃO ENVIADOS PARA A API
    params: Dict[str, str] = {
        "function": "TIME_SERIES_DAILY",  # DEFINE O ENDPOINT DE SÉRIE TEMPORAL DIÁRIA
        "symbol": symbol,  # DEFINE O TICKER DA AÇÃO CONSULTADA
        "apikey": api_key,  # CHAVE DE AUTENTICAÇÃO DA API
        "outputsize": outputsize,  # DEFINE O TAMANHO DO HISTÓRICO RETORNADO
    }

    # REALIZA A REQUISIÇÃO HTTP GET PARA A API COM TIMEOUT DE 10 SEGUNDOS
    response = requests.get(ALPHA_URL, params=params, timeout=10)

    # VERIFICA SE A RESPOSTA HTTP FOI BEM-SUCEDIDA
    if response.status_code != 200:
        # LANÇA UMA EXCEÇÃO CASO A API RETORNE UM CÓDIGO DE ERRO
        raise RuntimeError(f"API request failed: {response.status_code}")

    # CONVERTE A RESPOSTA JSON DA API PARA UM DICIONÁRIO PYTHON
    data: Dict[str, Any] = response.json()

    # VERIFICA SE A ESTRUTURA ESPERADA DE DADOS EXISTE NA RESPOSTA DA API
    if "Time Series (Daily)" not in data:
        # LANÇA UMA EXCEÇÃO CASO A ESTRUTURA DO JSON NÃO SEJA A ESPERADA
        raise RuntimeError(f"Unexpected API response: {data}")

    # EXTRAI OS METADADOS DA RESPOSTA DA API
    meta_data = data["Meta Data"]

    # EXTRAI O DATASET PRINCIPAL COM OS DADOS DIÁRIOS DA AÇÃO
    dataset = data["Time Series (Daily)"]

    # RECUPERA O CÓDIGO DA AÇÃO PRESENTE NOS METADADOS DA RESPOSTA
    symbol_meta: str = meta_data["2. Symbol"]

    # CONVERTE O DICIONÁRIO DE SÉRIE TEMPORAL EM UM DATAFRAME PANDAS
    df = (
        pd.DataFrame.from_dict(dataset, orient="index")
        # RENOMEIA AS COLUNAS PARA NOMES MAIS SIMPLES E PADRONIZADOS
        .rename(columns={
            "1. open": "open",
            "2. high": "high",
            "3. low": "low",
            "4. close": "close",
            "5. volume": "volume"
        })
    # DEFINE O NOME DO ÍNDICE COMO "DATE" E CONVERTE O ÍNDICE EM COLUNA
    ).rename_axis("date").reset_index()

    # INSERE A COLUNA DO SÍMBOLO DA AÇÃO NA SEGUNDA POSIÇÃO DO DATAFRAME
    df.insert(1, 'symbol', symbol_meta)

    # RETORNA O DATAFRAME ORDENADO CRONOLOGICAMENTE PELA DATA
    return df.sort_values('date')