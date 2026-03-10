# 📝 Notas do Projeto — ETL Gastos Parlamentares

## 🛠️ Ambiente

- Python 3.14.0
- Sistema Operacional: Windows
- Editor: VSCode
- Ambiente virtual: venv

## 📦 Bibliotecas instaladas

| Biblioteca | Para que serve |
|---|---|
| `requests` | Buscar dados da API da Câmara dos Deputados |
| `pandas` | Transformar e limpar os dados |
| `mysql-connector-python` | Conectar Python ao MySQL |
| `python-dotenv` | Carregar credenciais do .env |

## 🗃️ Fonte de Dados

- **API** — Gastos Públicos Parlamentar (dadosabertos.camara.leg.br)

## ❓ Pergunta Analítica do Projeto

"Qual o total gasto pelo parlamentar durante seu mandato?"

## 📌 Decisões Técnicas

- Credenciais do banco ficam no `.env` — nunca sobem pro GitHub
- `.env.example` sobe pro GitHub como modelo para a equipe
- Commits seguem padrão semântico: feat, fix, docs, refactor
- O arquivo `utils.py` será utilizado para guardar dados relevantes e reutilizados
- `None` é retornado em caso de exception e o retorno seja vazio

## 📦 Dependências

As bibliotecas instaladas trouxeram dependências automáticas.
Ver lista completa em `requirements.txt`.