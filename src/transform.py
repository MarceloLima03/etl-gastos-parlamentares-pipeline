import pandas as pd
from extract import buscar_deputados, buscar_gastos
from utils import ID_PARLAMENTAR, PERIODO

def transformar_dados_deputado(response):
    """
    Transforma os dados em DataFrame

    Args:
        response (response): Lista com todos os dados de despesas do deputado
    
    Returns:
        pd.DataFrame: DataFrame com os dados transformados
    """
    dados = response.json()['dados']
    dados_desejados = {
        'id': dados['id'],
        'nome': dados['nomeCivil'],
        'partido': dados['ultimoStatus']['siglaPartido'],
        'estado': dados['ultimoStatus']['siglaUf'],
        'email': dados['ultimoStatus']['gabinete']['email'],
        'nascimento': dados['dataNascimento'],
        'escolaridade': dados['escolaridade']
    }
    data_frame = pd.DataFrame([dados_desejados])
    return data_frame

def transformar_gastos(response):
    """
    Transforma os dados em DataFrame

    Args:
        response (response): Lista com todos os dados de despesas do deputado
    
    Returns:
        pd.DataFrame: DataFrame com os dados transformados
    
    Notes:
         datas inválidas são substituídas por 1990-01-01
    """
    data_frame = pd.DataFrame(response)
    data_frame.fillna({'urlDocumento': ''}, inplace=True)
    data_frame['dataDocumento'] = pd.to_datetime(data_frame['dataDocumento'], errors='coerce', dayfirst=True) 
    data_frame['dataDocumento'] = data_frame['dataDocumento'].fillna(pd.Timestamp('1990-01-01'))
    return data_frame
