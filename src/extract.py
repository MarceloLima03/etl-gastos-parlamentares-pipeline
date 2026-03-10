import requests
from utils import BASE_URL, ID_PARLAMENTAR, PERIODO


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