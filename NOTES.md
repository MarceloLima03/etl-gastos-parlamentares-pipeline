# 📝 Notas do Projeto — ETL IBGE Pipeline

## 🛠️ Ambiente

- Python 3.14.0
- Sistema Operacional: Windows
- Editor: VSCode
- Ambiente virtual: venv

## 📦 Bibliotecas instaladas

| Biblioteca | Para que serve |
|---|---|
| `requests` | Buscar dados da API do IBGE |
| `pandas` | Transformar e limpar os dados |
| `mysql-connector-python` | Conectar Python ao MySQL |
| `python-dotenv` | Carregar credenciais do .env |

## 🗃️ Fonte de Dados

- **CSV** — Bolsa Família por município (Portal da Transparência)
- **API** — Desemprego por estado (IBGE)

## ❓ Pergunta Analítica do Projeto

"Municípios com maior desemprego recebem mais Bolsa Família?"

## 📌 Decisões Técnicas

- Credenciais do banco ficam no `.env` — nunca sobem pro GitHub
- `.env.example` sobe pro GitHub como modelo para a equipe
- Commits seguem padrão semântico: feat, fix, docs, refactor

## 📦 Dependências

As bibliotecas instaladas trouxeram dependências automáticas.
Ver lista completa em `requirements.txt`.