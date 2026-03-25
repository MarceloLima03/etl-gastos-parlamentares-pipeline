import requests
from utils import BASE_URL
from urllib.parse import urlencode
from logging_config import logger
import logging
from tenacity import retry, stop_after_attempt, wait_fixed, after_log, retry_if_exception_type

@retry(stop=stop_after_attempt(3), 
       wait=wait_fixed(2), 
       after=after_log(logger, logging.WARNING),
       retry=(retry_if_exception_type(requests.exceptions.HTTPError) | 
              retry_if_exception_type(requests.exceptions.RequestException)),
              reraise=True)
def buscar_deputados(id):
    """
    Busca informações básicas de um deputado na API da Câmara.

    Args:
        id (int): ID do deputado na API da Câmara
    
    Returns:
        response: objeto Response com os dados do deputado
        None: se ocorrer algum erro na requisição
    """
    logger.info("Aguarde: Buscando dados do deputado...")
    try:
        response = requests.get(f'{BASE_URL}/deputados/{id}')
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        logger.error(f'HTTP error occurred:{e}')
        return None
    except requests.exceptions.RequestException as e:
        logger.error(f'A request error occurred:{e}')
        return None

    return response

@retry(stop=stop_after_attempt(3), 
       wait=wait_fixed(2), 
       after=after_log(logger, logging.WARNING),
       retry=(retry_if_exception_type(requests.exceptions.HTTPError) | 
              retry_if_exception_type(requests.exceptions.RequestException)),
              reraise=True)
def buscar_gastos(id, ano):
    """
    Busca as despesas de um parlamentar na API da Câmara.
    
    Args:
        id (int): ID do deputado na API da Câmara
        ano (tuple): Anos de referência ex: (2023, 2024, 2025)

    Returns:
        response: objeto Response com as despesas do deputado
    """
    logger.info("Aguarde: Buscando os gastos do deputado...")
    queryparameters = urlencode({'ano': ','.join(map(str, ano))})
    resp_completo = []
    next_page = True
    try:
        response = requests.get(f'{BASE_URL}/deputados/{id}/despesas?{queryparameters}&itens=100')
        response.raise_for_status()
        while next_page:
            dados = response.json()['dados']
            for dado in dados:
                resp_completo.append(dado)
            links = response.json()['links']
            for link in links:
                if link.get('rel') == 'next':
                    url = link.get('href')
                    response = requests.get(url)
                    response.raise_for_status()
                    break
                elif link.get('rel') == 'previous': 
                    next_page = False
    except requests.exceptions.HTTPError as e:
        logger.error(f'HTTP error occurred:{e}')
        return None
    except requests.exceptions.RequestException as e:
        logger.error(f'A request error occurred:{e}')
        return None
    
    return resp_completo