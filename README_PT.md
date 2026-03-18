# Plataforma de Dados Financeiros (cotações e indicadores)

Uma plataforma de dados ponta a ponta que ingere APIs públicas brasileiras e constrói conjuntos de dados prontos para análise utilizando ferramentas modernas do ecossistema de dados.

## 🎯 Visão Geral do Projeto

Este projeto demonstra um fluxo completo de engenharia de dados:
- **Ingestão de Dados**: APIs do mercado brasileiro (Alpha Vantage, BRAPI, Banco Central)
- **Data Warehouse**: PostgreSQL com schema estruturado (Bronze/Prata/Ouro)
- **Transformação de Dados**: dbt para construção de datasets prontos para análise
- **Orquestração**: Pipelines em Python com validações de qualidade de dados

## 🏗️ Arquitetura

```
APIs → Ingestão em Python → PostgreSQL (Bronze) → dbt (Silver/Gold)
```

### Stack Tecnológica
- **Linguagens**: Python 3.13+, SQL  
- **Processamento de Dados**: dbt-core 1.11.7, dbt-postgres  
- **Banco de Dados**: PostgreSQL 16  
- **Formatos de Dados**: Pandas, DuckDB, SQLAlchemy  
- **Infraestrutura**: Docker Compose  
- **Desenvolvimento**: uv (gerenciador de pacotes), SQLFluff  

## 📦 Estrutura do Projeto

```
finance-data-platform/
├── ingestion/           # Camada de pipeline de dados em Python
│   ├── data_fonts/      # Conectores de APIs
│   ├── pipelines/       # Fluxos ETL
│   └── utils/           # Utilitários de banco de dados
├── dbt_project/         # Camada de transformação com dbt
│   ├── models/
│   │   ├── bronze/      # Modelos de dados brutos
│   │   ├── silver/      # Dados tratados
│   │   └── gold/        # Tabelas prontas para negócio
│   ├── tests/           # Testes de qualidade de dados
│   └── macros/          # Funções customizadas do dbt
├── docker-compose.yml   # Configuração do PostgreSQL + volume
└── pyproject.toml       # Gerenciamento de dependências
```

## 🚀 Primeiros Passos

### Pré-requisitos
- Python 3.13+
- Docker e Docker Compose
- uv (ou pip)

### Instalação

```bash
# Instalar dependências
uv sync

# Subir o PostgreSQL
docker-compose up -d

# Verificar conexão com o banco
```

### Executando o Pipeline

```bash
# Executar ingestão
python ingestion/pipeline.py

# Rodar transformações com dbt
cd dbt_project
dbt run
dbt test
```

## 📊 Modelos de Dados

### Camada Bronze
- `bronze_alphavantage__stock_prices_daily`: Dados brutos de ações
- `bronze__symbol_countries`: Metadados dos ativos

### Camada Prata
- `silver_alphavantage__stock_prices_daily`: Preços tratados e sem duplicidade
- `silver_symbol_countries`: Símbolos padronizados

### Camada Ouro
- Agregações analíticas e métricas de negócio prontas para uso

## 🔑 Principais Características

✅ Arquitetura de pipeline modular  
✅ Linhagem completa de dados com dbt  
✅ Python com tipagem e ferramentas modernas  
✅ Containerização com Docker  
✅ Padronização SQL com SQLFluff  
✅ Estrutura extensível para novas fontes de dados  

## 📝 Desenvolvimento

```bash
# Formatar SQL
sqlfluff format

# Validar e analisar SQL
sqlfluff lint dbt_project/models/

# Executar testes
dbt test
```

## 📮 Contato

Projeto criado para demonstração de boas práticas em engenharia de dados.
