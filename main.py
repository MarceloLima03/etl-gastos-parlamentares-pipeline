import sys
sys.path.append("src")
from extract import buscar_deputados, buscar_gastos
from transform import transformar_dados_deputado, transformar_gastos
from load import conexao, criar_tabelas, inserir_deputado, inserir_gastos
from utils import ID_PARLAMENTAR, PERIODO
from logging_config import logger

def executar_pipeline():
    conn = conexao()
    try:
        criar_tabelas(conn)

        response = buscar_deputados(ID_PARLAMENTAR)
        data_frame_deputados = transformar_dados_deputado(response)
        inserir_deputado(conn, data_frame_deputados)

        response = buscar_gastos(ID_PARLAMENTAR, PERIODO)
        data_frame_gastos = transformar_gastos(response)
        id_deputado = int(data_frame_deputados['id'].iloc[0])
        inserir_gastos(conn, data_frame_gastos, id_deputado)
    finally:
        if conn is not None:
            try:
                conn.close()
                logger.info('Aguarde: Fechando conexão com o banco...')
            except Exception as e:
                logger.error(f'Erro ao fechar conexão: {e}')

if __name__ == '__main__':
    executar_pipeline()