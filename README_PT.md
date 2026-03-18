# Plataforma de Dados Financeiros

Uma plataforma de dados de ponta a ponta que ingere APIs públicas brasileiras e constrói conjuntos de dados prontos para análise usando ferramentas modernas de data stack.

## 🎯 Visão Geral do Projeto

Este projeto demonstra um fluxo completo de engenharia de dados seguindo o padrão de arquitetura medallion:
- **Ingestão de Dados**: APIs do mercado brasileiro (Alpha Vantage, BRAPI, Banco Central)
- **Data Warehouse**: PostgreSQL com esquema estruturado em camadas (Bronze/Silver/Gold)
- **Transformação de Dados**: dbt para construir conjuntos de dados prontos para análise
- **Orquestração**: Pipelines em Python com verificações de qualidade de dados

## 🏗️ Arquitetura

```
APIs → Ingestão em Python → PostgreSQL (Bronze) → Transformações dbt (Silver/Gold) → Analytics
```

### Arquitetura de Camadas Medallion

A plataforma segue uma arquitetura medallion de três camadas:

- **Camada Bronze**: Dados brutos, não modificados, ingeridos diretamente das APIs. Serve como fonte única de verdade para todos os dados brutos, com transformações mínimas.
- **Camada Silver**: Conjuntos de dados limpos, deduplicados e padronizados. Aplicam-se verificações de qualidade de dados, tratamento de valores nulos, e as regras de negócio começam a surgir.
- **Camada Gold**: Conjuntos de dados agregados e prontos para análise, otimizados para relatórios e business intelligence. Contém métricas calculadas, dimensões de negócio e KPIs prontos para consumo.

### Stack Tecnológico
- **Linguagens**: Python 3.12+, SQL
- **Processamento de Dados**: dbt-core 1.11.7, dbt-postgres
- **Banco de Dados**: PostgreSQL 16
- **Formatos de Dados**: Pandas, DuckDB, SQLAlchemy
- **Infraestrutura**: Docker Compose
- **Desenvolvimento**: uv (gerenciador de pacotes), SQLFluff

## 📦 Estrutura do Projeto

```
finance-data-platform/
├── ingestion/           # Camada de pipelines em Python
│   ├── data_fonts/     # Conectores de APIs
│   ├── pipelines/      # Workflows ETL
│   └── utils/          # Utilitários de banco de dados
├── dbt_project/        # Camada de transformação dbt
│   ├── models/
│   │   ├── bronze/     # Modelos de dados brutos
│   │   ├── silver/     # Conjuntos de dados limpos e padronizados
│   │   └── gold/       # Tabelas analíticas prontas para negócio
│   ├── tests/          # Testes de qualidade de dados
│   └── macros/         # Funções customizadas dbt
├── docker-compose.yml  # Configuração PostgreSQL + volumes
└── pyproject.toml      # Gerenciamento de dependências
```

## 🚀 Iniciando

### Pré-requisitos
- Python 3.12+
- Docker & Docker Compose
- uv (ou pip)

### Instalação

```bash
# Instalar dependências
uv sync

# Iniciar PostgreSQL
docker-compose up -d

# Verificar conexão com o banco
```

### Executando o Pipeline

```bash
# Executar ingestão
python main.py

# Executar transformações dbt
cd dbt_project
dbt run
dbt test

# Gerar e servir documentação
python build.py
```

## 📊 Modelos de Dados

### Camada Bronze
Dados brutos ingeridos diretamente das APIs, com transformações mínimas. Funciona como um data lakehouse para todos os sistemas de origem.

- `bronze_alphavantage__stock_prices_daily`: Dados brutos de preços de ações (OHLCV)
- `bronze_brapi__stock_prices_daily`: Preços de ações brasileiras do BRAPI
- `bronze__symbol_countries`: Metadados brutos e mapeamentos de símbolos

**Objetivo**: Registro histórico imutável; permite auditoria e recuperação de dados.

### Camada Silver
Conjuntos de dados limpos, deduplicados e validados com regras de negócio aplicadas. Verificações de qualidade garantem consistência.

- `silver_alphavantage__stock_prices_daily`: Preços deduplicados e limpos, com tratamento de valores nulos
- `silver_brapi__stock_prices_daily`: Preços do mercado brasileiro padronizados
- `silver__symbol_countries`: Dados de referência de símbolos validados

**Objetivo**: Base de dados padronizada para análises; fonte única de verdade para dados confiáveis.

### Camada Gold
Tabelas analíticas agregadas e prontas para negócio, otimizadas para relatórios e tomada de decisão.

**Tabelas Analíticas**:
- `gold_daily_returns`: Cálculos de retorno diário (absoluto e percentual) agregados por símbolo
- `gold_market_indicators__economic`: Indicadores econômicos do Banco Central (taxas de juros, inflação, câmbio)
- `gold_market_performance__aggregated`: Métricas e índices de performance do mercado

**Principais Métricas & Agregações**:
- Retornos percentuais diários e cálculos de volatilidade
- Movimentações e tendências gerais de mercado
- Séries temporais de indicadores econômicos para análises de correlação
- Rankings e comparações de desempenho por símbolo

**Objetivo**: Permitir que stakeholders e analistas acessem métricas pré-calculadas sem joins complexos; reduzir latência de consultas para dashboards e relatórios.

## 🔑 Principais Recursos

✅ Arquitetura modular de pipelines  
✅ Linha completa de dados com dbt  
✅ Python type-safe com ferramentas modernas  
✅ Containerização com Docker  
✅ Linting de SQL com SQLFluff  
✅ Estrutura extensível para fontes de dados  
✅ Testes automáticos de qualidade de dados  
✅ Arquitetura medallion pronta para produção  

## 📝 Desenvolvimento

```bash
# Formatar SQL
sqlfluff format dbt_project/

# Lint e validação
sqlfluff lint dbt_project/models/

# Executar testes de qualidade de dados
dbt test

# Gerar documentação
dbt docs generate
dbt docs serve --port 8081
```

## 📮 Contato

Criado para demonstrar as melhores práticas de engenharia de dados em plataformas de analytics modernas.

