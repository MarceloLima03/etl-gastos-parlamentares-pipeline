import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def conexao():
    """
    Abrir conexão com o banco de dados

    Returns:
        psycopg2.connect - conexão aberta com o banco PostgreSQL
    """
    print("Aguarde: Abrindo conexão com o banco...")
    conn = psycopg2.connect(
        host=os.getenv('DB_HOST'),
        database=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        port=os.getenv('DB_PORT')
    )

    return conn

def criar_tabelas(conn):
    """
    Lê o arquivo create_tables.sql e cria as tabelas 

    Args:
        conn (conexão psycopg2): Conexão com o banco
    """
    print("Aguarde: Criando tabela no banco...")
    try:
        cursor = conn.cursor()

        with open('sql/create_tables.sql', mode='r', encoding='utf-8') as arquivo:
            conteudo_sql = arquivo.read()
            cursor.execute(conteudo_sql)
            conn.commit()
    except psycopg2.Error as e:
        print(f'Erro de conexão: {e}')
    finally:
        if cursor is not None:
            try:
                cursor.close()
            except psycopg2.Error as e:
                print(f'Erro ao fechar cursor: {e}')

def inserir_deputado(conn, data_frame_deputado):
    """
    Insere os dados do data_frame dados do deputado 

    Args:
        conn (conexão psycopg2): Conexão com o banco
        data_frame_deputado (dataFrame): dataFrame padronizado
    """
    print("Aguarde: Inserindo dados na tabela dim_deputados...")
    try:
        cursor = conn.cursor()
        for _, row in data_frame_deputado.iterrows():
            cursor.execute("""
                INSERT INTO dim_deputados(ID_DEPUTADO, NOME, PARTIDO, ESTADO, EMAIL, NASCIMENTO, ESCOLARIDADE)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (ID_DEPUTADO) DO NOTHING;""",
                (row['id'], row['nome'], row['partido'], row['estado'], row['email'], row['nascimento'], row['escolaridade'])
            )
        conn.commit()
    except psycopg2.Error as e:
        print(f'Erro ao fechar cursor: {e}')
    finally:
        if cursor is not None:
            try:
                cursor.close()
            except psycopg2.Error as e:
                print(f'Erro ao fechar cursor: {e}')

def inserir_gastos(conn, data_frame_gastos, id_deputado):
    """
    Insere os gastos do data_frame gastos do deputado 

    Args:
        conn (conexão psycopg2): Conexão com o banco
        data_frame_gastos (dataFrame): dataFrame padronizado
        id_deputado (int): ID do deputado
    """
    print("Aguarde: Inserindo dados na tabela fact_gastos...")
    try:
        cursor = conn.cursor()
        for _, row in data_frame_gastos.iterrows():
            cursor.execute("""
                INSERT INTO fact_gastos(
                           ID_DEPUTADO, ANO, MES, TIPO_DESPESA, COD_DOCUMENTO, TIPO_DOCUMENTO, COD_TIPO_DOCUMENTO,
                           DATA_DOCUMENTO, NUM_DOCUMENTO, VALOR_DOCUMENTO, URL_DOCUMENTO, NOME_FORNECEDOR, 
                           CNPJ_FORNECEDOR, VALOR_LIQUIDO, VALOR_GLOSA, NUM_RESSARCIMENTO, COD_LOTE, PARCELA)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                (id_deputado, row['ano'], row['mes'], row['tipoDespesa'], row['codDocumento'], row['tipoDocumento'], row['codTipoDocumento'],
                 row['dataDocumento'].to_pydatetime(), row['numDocumento'], row['valorDocumento'], row['urlDocumento'], row['nomeFornecedor'], row['cnpjCpfFornecedor'], 
                 row['valorLiquido'], row['valorGlosa'], row['numRessarcimento'], row['codLote'], row['parcela'])
            )
        conn.commit()
    except psycopg2.Error as e:
        print(f'Erro ao fechar cursor: {e}')
    finally:
        if cursor is not None:
            try:
                cursor.close()
            except psycopg2.Error as e:
                print(f'Erro ao fechar cursor: {e}')