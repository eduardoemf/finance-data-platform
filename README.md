
# Finance Data Platform

An end-to-end data platform that ingests Brazilian public APIs and builds analytics-ready datasets using modern data stack tools.

## 🎯 Project Overview

This project demonstrates a complete data engineering workflow:
- **Data Ingestion**: Brazilian market APIs (Alpha Vantage, BRAPI, Banco Central)
- **Data Warehouse**: PostgreSQL with structured schema (Bronze/Silver/Gold)
- **Data Transformation**: dbt for building analytics-ready datasets
- **Orchestration**: Python-based pipelines with data quality checks

## 🏗️ Architecture

```
APIs → Python Ingestion → PostgreSQL (Bronze) → dbt (Silver/Gold)
```

### Tech Stack
- **Languages**: Python 3.13+, SQL
- **Data Processing**: dbt-core 1.11.7, dbt-postgres
- **Database**: PostgreSQL 16
- **Data Formats**: Pandas, DuckDB, SQLAlchemy
- **Infrastructure**: Docker Compose
- **Development**: uv (package manager), SQLFluff

## 📦 Project Structure

```
finance-data-platform/
├── ingestion/           # Python data pipeline layer
│   ├── data_fonts/     # API connectors
│   ├── pipelines/      # ETL workflows
│   └── utils/          # Database utilities
├── dbt_project/        # dbt transformation layer
│   ├── models/
│   │   ├── bronze/     # Raw data models
│   │   ├── silver/     # Cleaned datasets
│   │   └── gold/       # Business-ready tables
│   ├── tests/          # Data quality tests
│   └── macros/         # Custom dbt functions
├── docker-compose.yml  # PostgreSQL + volume setup
└── pyproject.toml      # Dependencies management
```

## 🚀 Getting Started

### Prerequisites
- Python 3.13+
- Docker & Docker Compose
- uv (or pip)

### Installation

```bash
# Install dependencies
uv sync

# Start PostgreSQL
docker-compose up -d

# Verify database connection
```

### Running the Pipeline

```bash
# Execute ingestion
python ingestion/pipeline.py

# Run dbt transformations
cd dbt_project
dbt run
dbt test
```

## 📊 Data Models

### Bronze Layer
- `bronze_alphavantage__stock_prices_daily`: Raw stock data
- `bronze__symbol_countries`: Symbol metadata

### Silver Layer
- `silver_alphavantage__stock_prices_daily`: Cleaned, deduplicated prices
- `silver_symbol_countries`: Standardized symbols

### Gold Layer
- Analytics-ready aggregations and business metrics

## 🔑 Key Features

✅ Modular pipeline architecture  
✅ Comprehensive data lineage with dbt  
✅ Type-safe Python with modern tooling  
✅ Docker containerization  
✅ SQL linting with SQLFluff  
✅ Extensible data source framework  

## 📝 Development

```bash
# Format SQL
sqlfluff format

# Lint & validate
sqlfluff lint dbt_project/models/

# Run tests
dbt test
```

## 📮 Contact

Created for demonstration of data engineering best practices.
