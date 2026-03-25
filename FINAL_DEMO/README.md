# Financial ETL Project

An Apache Airflow-based ETL (Extract, Transform, Load) project for financial risk data processing with machine learning capabilities.

## Features

- **Apache Airflow 2.8.1**: Orchestrate complex data workflows
- **Poetry**: Modern Python dependency management
- **Docker**: Containerized deployment with docker-compose
- **Security**: Latest patched versions addressing known CVEs

## Requirements

- Python 3.12+

- Docker & Docker Compose (for containerized deployment)
## Docker Deployment

```bash
# Build and start all services
docker compose build 
docker-compose up -d

# Access Airflow UI
# URL: http://localhost:8079
# Username: admin
# Password: admin
```
final_demo/
├── dags/                   # Airflow DAG definitions
├── scripts/                # ETL modules
│   ├── extract_fin_risk_csv.py         # Data extraction
│   ├── train_risk_model.py       # Processing & ML
│   └── load.py            # Database loading
├── scripts/               # Utility scripts
├── requirements.txt       # Pip requirements (fallback)
├── Dockerfile             # Container definition
└── docker-compose.yaml    # Multi-service orchestration
```