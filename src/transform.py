import pandas as pd
from extract import buscar_gastos
from utils import ID_PARLAMENTAR, PERIODO

def transformar_gastos(dados):
    """
    Transforma os dados em DataFrame

    Args:
        dados (list): Lista com todos os dados de despesas do deputado
    
    Returns:
        pd.DataFrame: DataFrame com os dados transformados
    
    Notes:
         datas inválidas são substituídas por 1990-01-01
    """
    data_frame = pd.DataFrame(dados)
    data_frame.fillna({'urlDocumento': ''}, inplace=True)
    data_frame['dataDocumento'] = pd.to_datetime(data_frame['dataDocumento'], errors='coerce', dayfirst=True) 
    data_frame['dataDocumento'] = data_frame['dataDocumento'].fillna(pd.Timestamp('1990-01-01'))
    return data_frame

response = buscar_gastos(ID_PARLAMENTAR, PERIODO)
data_frame = transformar_gastos(response)