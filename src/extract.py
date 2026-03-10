import requests
from utils import BASE_URL, ID_PARLAMENTAR, PERIODO
from urllib.parse import urlencode


def buscar_deputados(id):
    """
    Busca informações básicas de um deputado na API da Câmara.

    Args:
        id (int): ID do deputado na API da Câmara
    
    Returns:
        response: objeto Response com os dados do deputado
        None: se ocorrer algum erro na requisição
    """
    try:
        response = requests.get(f'{BASE_URL}/deputados/{id}')
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print(f'HTTP error occurred:{e}')
        return None
    except requests.exceptions.RequestException as e:
        print(f'A request error occurred:{e}')
        return None

    return response

def buscar_gastos(id, ano):
    """
    Busca as despesas de um parlamentar na API da Câmara.
    
    Args:
        id (int): ID do deputado na API da Câmara
        ano (tuple): Anos de referência ex: (2023, 2024, 2025)

    Returns:
        response: objeto Response com as despesas do deputado
    """
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
        print(f'HTTP error occurred:{e}')
        return None
    except requests.exceptions.RequestException as e:
        print(f'A request error occurred:{e}')
        return None
    
    return resp_completo