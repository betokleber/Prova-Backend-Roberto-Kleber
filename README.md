### testes efetuados no codespace P2Roberto Kleber

# P2 Backend - Sistema Modular de E-Commerce
## 🐳 1. Instruções para Subir o Banco de Teste com Docker

O projeto utiliza dois containers separados para garantir que o ambiente de desenvolvimento não interfira nos testes automatizados. O banco dedicado aos testes roda isolado na porta `5433`.

Certifique-se de possuir o Docker e o Docker Compose instalados em sua máquina e execute o comando abaixo na raiz do repositório para inicializar o serviço:

```bash
docker-compose up -d db_test

Passo 1
1. Realoque seus arquivos conforme a nova estrutura modular indicada no seu prompt.
2. Ative seu ambiente virtual do Python e instale as dependências:
   ```bash
   pip install -r requirements.txt

Passo 2 
Executar Containers Docker
Inicialize os containers do banco de dados em plano de fundo:

Bash
docker-compose up -d

Passo 3
Executar os Testes

Bash
pytest --cov=app -v

# 🛒 API P2 Backend - Sistema de Catálogo de E-Commerce

Esta é uma API RESTful  desenvolvida com **FastAPI**, **SQLAlchemy ORM** e **Pydantic**, estruturada de forma modular (Camadas de Repositório, Serviço e Roteamento) com suporte a migrações e persistência em banco de dados **PostgreSQL real via Docker**.

Para cumprir a regra de "banco real com isolamento total" e mitigar o risco de efeitos colaterais (onde o estado gerado por um teste interfere no resultado do próximo), a arquitetura utiliza o ciclo de vida de fixtures do pytest no arquivo central conftest.py:

Escopo por Função (scope="function"): A fixture client é reinicializada individualmente para cada função de teste executada.

Estratégia de Setup: Antes do teste rodar, o comando Base.metadata.create_all(bind=engine_test) reconstrói do zero todas as tabelas na base de dados PostgreSQL de testes (ecom_test).

Injeção de Dependência: O mecanismo app.dependency_overrides do FastAPI intercepta o gerenciador de sessões original (get_db) e força o uso do banco de testes transacional.

Estratégia de Teardown: Logo após a finalização do teste, o bloco após o yield executa o comando Base.metadata.drop_all(bind=engine_test). Isso elimina completamente todas as tabelas e dados gerados, entregando um banco de dados totalmente limpo para a próxima função.
---



