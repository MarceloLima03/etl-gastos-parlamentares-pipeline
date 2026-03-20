# 📝 Notas do Projeto — ETL Gastos Parlamentares

## 🛠️ Ambiente

- Python 3.14.0
- Sistema Operacional: Windows
- Editor: VSCode
- Ambiente virtual: venv
- Banco de dados: PostgreSQL (via Docker)

---

## 📦 Bibliotecas instaladas

| Biblioteca | Para que serve |
|---|---|
| `requests` | Buscar dados da API da Câmara dos Deputados |
| `pandas` | Transformar e limpar os dados |
| `psycopg2-binary` | Conectar Python ao PostgreSQL |
| `python-dotenv` | Carregar credenciais do .env |
| `apscheduler` | Agendamento do pipeline |

---

## 🗃️ Fonte de Dados

- **API** — Câmara dos Deputados
- URL base: `https://dadosabertos.camara.leg.br/api/v2`
- Swagger: `https://dadosabertos.camara.leg.br/swagger/api.html`
- Sem necessidade de cadastro ou chave de API

---

## 👤 Parlamentar monitorado

- **Nome:** Nikolas Ferreira
- **ID na API:** 209787
- **Legislatura ativa:** 57 (2023-2027)
- **Anos monitorados:** 2023, 2024, 2025

---

## ❓ Pergunta Analítica do Projeto

"Qual o total gasto pelo parlamentar durante seu mandato?"

---

## 🏗️ Estrutura do Projeto

```
etl-gastos-parlamentares-pipeline/
│
├── src/
│   ├── extract.py       → busca dados da API
│   ├── transform.py     → limpa e organiza os dados
│   ├── load.py          → salva no PostgreSQL
│   ├── utils.py         → configurações compartilhadas
│   └── __init__.py
│
├── sql/
│   └── create_tables.sql  → cria tabelas no PostgreSQL
│
├── main.py              → orquestra o pipeline
├── Dockerfile           → empacota o pipeline
├── docker-compose.yml   → orquestra pipeline + PostgreSQL
├── .env                 → credenciais (nunca sobe pro GitHub)
├── .env.example         → modelo público das variáveis
├── .gitignore           → arquivos ignorados pelo Git
├── requirements.txt     → dependências do projeto
└── NOTES.md             → documentação do projeto
```

---

## 🔄 Fluxo do Pipeline

```
API Câmara dos Deputados
        ↓
    extract.py
    ├── buscar_deputados(id)
    └── buscar_gastos(id, anos)  → paginação automática
        ↓
   transform.py
    ├── transformar_dados_deputado(response)
    └── transformar_gastos(response)
        ↓
      load.py
    ├── conexao()
    ├── criar_tabelas(conn)
    ├── inserir_deputado(conn, df)
    └── inserir_gastos(conn, df, id_deputado)
        ↓
    PostgreSQL (Docker)
    ├── dim_deputados
    └── fact_gastos
```

---

## 🗄️ Modelo Dimensional

### DIM_DEPUTADOS
```sql
ID_DEPUTADO  INT PRIMARY KEY      -- ID vem da API
NOME         TEXT
PARTIDO      TEXT
ESTADO       TEXT
EMAIL        TEXT
NASCIMENTO   DATE
ESCOLARIDADE TEXT
```

### FACT_GASTOS
```sql
ID_GASTOS          SERIAL PRIMARY KEY
ID_DEPUTADO        INT REFERENCES dim_deputados
ANO                INT
MES                INT
TIPO_DESPESA       TEXT
COD_DOCUMENTO      TEXT
TIPO_DOCUMENTO     TEXT
COD_TIPO_DOCUMENTO INT
DATA_DOCUMENTO     TIMESTAMP
NUM_DOCUMENTO      TEXT
VALOR_DOCUMENTO    NUMERIC(10,2)
URL_DOCUMENTO      TEXT
NOME_FORNECEDOR    TEXT
CNPJ_FORNECEDOR    TEXT
VALOR_LIQUIDO      NUMERIC(10,2)
VALOR_GLOSA        NUMERIC(10,2)
NUM_RESSARCIMENTO  TEXT
COD_LOTE           INT
PARCELA            INT
```

---

## 📌 Decisões Técnicas — Pipeline

- Credenciais do banco ficam no `.env` — nunca sobem pro GitHub
- `.env.example` sobe pro GitHub como modelo para a equipe
- Commits seguem padrão semântico: `feat`, `fix`, `docs`, `refactor`
- `utils.py` guarda configurações compartilhadas entre os arquivos
- `None` é retornado em caso de exception
- `ID_DEPUTADO` vem da API — não é gerado pelo banco
- Conexão é aberta no `main.py` e fechada no `finally`
- Tipos numpy convertidos para tipos nativos Python antes do INSERT
- `psycopg2` requer `commit()` explícito após INSERT
- `ON CONFLICT (ID_DEPUTADO) DO NOTHING` evita duplicatas no deputado

---

## 🐳 Decisões Técnicas — Docker

- Migrado de SQL Server para PostgreSQL — melhor suporte Docker e open source
- Porta exposta como `5433` para evitar conflito com processos locais
- `healthcheck` garante que pipeline só inicia após banco estar pronto
- `restart: no` — pipeline ETL roda uma vez e termina
- Volume `pgdata` persiste dados entre reinicializações do container
- Variáveis sensíveis usam `${}` no docker-compose — valores ficam no `.env`
- `.env` sem aspas nos valores — docker-compose não interpreta aspas corretamente

---

## 🔐 Variáveis de Ambiente (.env)

```
DB_HOST=database
DB_NAME=gastos_parlamentares
DB_USER=postgres
DB_PASSWORD=sua_senha
DB_PORT=5432
```

---

## 📦 Dependências

Ver lista completa em `requirements.txt`.

---

## 🗺️ Roadmap Completo

### FASE 1 — Consolidar o projeto atual (3-4 semanas)
> Objetivo: transformar o pipeline em projeto maduro e bem documentado

- [x] Pipeline ETL funcionando (Extract, Transform, Load)
- [x] Modelo dimensional (dim_deputados + fact_gastos)
- [x] Credenciais protegidas com `.env`
- [x] Commits semânticos e repositório no GitHub
- [x] Automatizar com APScheduler
- [ ] Substituir `print()` por `logging` estruturado
- [ ] Adicionar retry nas chamadas de API
- [ ] README profissional com diagrama de arquitetura
- [ ] Expandir para múltiplos deputados

**Entregável:** Projeto limpo, documentado e funcional no GitHub.

---

### FASE 2 — Containerizar com Docker (2-3 semanas)
> Objetivo: eliminar dependência do ambiente Windows e SQL Server local

- [x] Criar `Dockerfile` para o pipeline
- [x] Subir pipeline + PostgreSQL com `docker-compose`
- [x] Migrar de SQL Server para PostgreSQL
- [x] Garantir que `docker-compose up` sobe tudo do zero

**Entregável:** Qualquer pessoa clona o repo e executa `docker-compose up`. ✅

---

### FASE 3 — Orquestrar com Apache Airflow (3-4 semanas)
> Objetivo: substituir APScheduler por DAGs versionados e monitorados

- [ ] Subir Airflow localmente via Docker Compose
- [ ] Converter o ETL em DAG com PythonOperator
- [ ] Configurar agendamento diário ou semanal
- [ ] Adicionar alertas de falha por e-mail

**Entregável:** Pipeline rodando no Airflow com DAG versionado e alertas ativos.

---

### FASE 4 — Transformar com dbt (3-4 semanas)
> Objetivo: organizar transformações SQL em camadas com testes de qualidade

- [ ] Instalar `dbt-postgres` e criar projeto
- [ ] Migrar transformações pandas para models SQL
  - `stg_gastos` → limpeza bruta
  - `int_gastos_por_deputado` → agregações
  - `mart_gastos_mensais` → tabela final
- [ ] Adicionar testes nativos (not_null, unique, accepted_values)
- [ ] Integrar dbt ao DAG do Airflow

**Entregável:** Camadas staging/mart no banco com testes passando e docs publicados.

---

### FASE 5 — Subir para AWS (4-6 semanas)
> Objetivo: migrar o pipeline para a nuvem

- [ ] Data lake no S3 com boto3
- [ ] Consultas com Amazon Athena + Glue Data Catalog
- [ ] Pipeline no ECR + ECS Fargate
- [ ] Airflow gerenciado com Amazon MWAA (opcional)

**Entregável:** Pipeline completo rodando na nuvem — S3 + Athena + ECS + Airflow.

---

## ✅ Status das Partes

| Parte | Descrição | Status |
|---|---|---|
| Parte 1 | Configurar ambiente | ✅ Concluído |
| Parte 2 | Extract — buscar dados da API | ✅ Concluído |
| Parte 3 | Transform — limpar dados | ✅ Concluído |
| Parte 4 | Load — salvar no banco | ✅ Concluído |
| Parte 5 | Automatizar com APScheduler | ✅ Concluído |
| Parte 6 | README profissional | 🔄 Pendente |

---

## 🚀 Próximos Passos Imediatos

- [x] Automatizar pipeline com `APScheduler`
- [x] Containerizar com Docker
- [x] Migrar de SQL Server para PostgreSQL
- [ ] Adicionar `logging` profissional (substituir prints)
- [ ] Escrever README com diagrama de arquitetura
- [ ] Expandir para múltiplos deputados
- [ ] Migrar orquestração para Apache Airflow
- [ ] Adicionar transformações com dbt
- [ ] Deploy na AWS

---

## 🧠 Conceitos Aprendidos

| Conceito | Onde foi aplicado |
|---|---|
| ETL | Pipeline completo extract → transform → load |
| Modelagem dimensional | dim_deputados + fact_gastos |
| API REST + paginação | buscar_gastos com loop de páginas |
| Ambiente virtual | venv isolando dependências |
| Variáveis de ambiente | .env + python-dotenv |
| Docker | Dockerfile + docker-compose |
| PostgreSQL | Banco relacional open source |
| Git semântico | feat, fix, docs, refactor |
| Clean Code | Funções pequenas, docstrings, PEP 8 |
