import pyodbc
import os
from dotenv import load_dotenv

load_dotenv()
def criar_tabelas():
    conn_str = (
        rf"DRIVER={os.getenv('DRIVER')};"
        rf"SERVER={os.getenv('SERVER')};"
        rf"TRUSTED_CONNECTION={os.getenv('TRUSTED_CONNECTION')}"
    )

    try:
        conn = pyodbc.connect(conn_str, autocommit=True)
        cursor = conn.cursor()

        with open('sql/create_tables.sql', mode='r', encoding='utf-8') as arquivo:
            conteudo_sql = arquivo.read()

        for bloco in conteudo_sql.split('GO'):
            if bloco:
                print(f"Executando: {bloco}")
                cursor.execute(bloco)
    except pyodbc.Error as e:
        print(f'Erro de conexão: {e}')
    finally:
        if cursor is not None:
            try:
                cursor.close()
            except pyodbc.Error as e:
                print(f'Erro ao fechar cursor: {e}')
        
        if conn is not None:
            try:
                conn.close()
            except pyodbc.Error as e:
                print(f'Erro ao fechar conexão: {e}')