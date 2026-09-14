# 🚀 Cloud-Native URL Shortener & Analytics

[![CI/CD Pipeline](https://github.com/erenakg/cloud-native-url-shortener/actions/workflows/ci.yml/badge.svg)](https://github.com/erenakg/cloud-native-url-shortener/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.11](https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110.0-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Docker](https://img.shields.io/badge/Docker-Enabled-2496ED?logo=docker&logoColor=white)](https://www.docker.com/)
[![Terraform](https://img.shields.io/badge/IaC-Terraform-7B42BC?logo=terraform&logoColor=white)](https://www.terraform.io/)
[![AWS LocalStack](https://img.shields.io/badge/AWS-LocalStack_Emulated-FF9900?logo=amazon-aws&logoColor=white)](https://localstack.cloud/)

A production-grade, containerized URL shortening and analytics microservice built with **FastAPI**, **Redis**, and emulated **AWS Cloud Services (S3, DynamoDB)** via **LocalStack**. 

This project demonstrates modern cloud-native software engineering and DevOps principles: zero-cloud-cost local cloud emulation, Infrastructure as Code (IaC) with **Terraform**, multi-container orchestration with **Docker Compose**, and automated continuous integration via **GitHub Actions**.

---

## 🏛️ System Architecture

```mermaid
flowchart TD
    subgraph ClientLayer["Client & Consumers"]
        Client["HTTP Client / Browser"]
    end

    subgraph DockerBridge["Docker Network (url-shortener-network)"]
        subgraph AppService["FastAPI Application (Port 8000)"]
            API["FastAPI Core Engine"]
            Router["API Router / Endpoints"]
            API --> Router
        end

        subgraph CacheService["In-Memory Cache (Port 6379)"]
            Redis[("Redis In-Memory Key-Value")]
        end

        subgraph LocalCloud["LocalStack Cloud Emulation (Port 4566)"]
            DynamoDB[("AWS DynamoDB Table<br/>ShortenedURLs")]
            S3[("AWS S3 Bucket<br/>cloud-url-shortener-data")]
        end
    end

    subgraph CI_CD["CI/CD Pipeline (GitHub Actions)"]
        Runner["Ubuntu Runner"]
        Pytest["Pytest Unit Test Suite"]
        DockerBuild["Docker Build & Validation"]
        Runner --> Pytest --> DockerBuild
    end

    Client -->|1. POST /shorten or GET /{code}| Router
    Router -->|2. Check Cache / Rate Limit| Redis
    Router -->|3. Persist / Query URL Metadata| DynamoDB
    Router -->|4. Export Metrics / Raw Logs| S3
```

---

## ✨ Key Features & Architectural Highlights

* **High-Performance Asynchronous Core:** Built on FastAPI (Python 3.11) utilizing asynchronous request handling and Pydantic validation schemas.
* **Sub-Millisecond Read Latency:** Leverages Redis 7 in-memory caching to resolve URL redirects instantly before falling back to persistent storage.
* **Zero-Cost AWS Cloud Emulation:** Fully integrated with LocalStack 3.4 to emulate AWS DynamoDB and S3 environments locally without deploying paid cloud infrastructure during development.
* **Infrastructure as Code (IaC):** AWS resources are declaratively defined, provisioned, and managed using Terraform (`provider.tf`, `main.tf`, `outputs.tf`) targeting LocalStack endpoints with path-style S3 access.
* **Containerization & Orchestration:** Fully containerized setup governed by Docker Compose with isolated bridge networks, health checks, and persistent volumes.
* **Automated CI/CD Pipeline:** GitHub Actions workflow executing unit tests via Pytest alongside an active Redis test service container and validating multi-stage Docker builds on every pull request.
* **Git Flow & Conventional Commits:** Strict branch management (`feature/*`, `chore/*`) and standardized semantic commits (`feat`, `fix`, `ci`, `chore`).

---

## 🛠️ Tech Stack

| Domain | Technologies |
|---|---|
| **Backend & API** | Python 3.11, FastAPI, Uvicorn, Pydantic, HTTPX |
| **Caching & Persistence** | Redis 7, AWS DynamoDB (LocalStack) |
| **Object Storage** | AWS S3 (LocalStack) |
| **Infrastructure as Code** | Terraform (HashiCorp AWS Provider ~> 5.0) |
| **Containerization** | Docker, Docker Compose |
| **CI / CD Pipeline** | GitHub Actions (Ubuntu Runners, Test Services) |
| **Quality Assurance** | Pytest |

---

## 📂 Directory Structure

```text
cloud-native-url-shortener/
├── .github/
│   └── workflows/
│       └── ci.yml                 # GitHub Actions CI workflow
├── app/
│   ├── main.py                    # FastAPI application & Redis integration
│   ├── test_main.py               # Unit & integration test suite
│   └── requirements.txt           # Python runtime and testing dependencies
├── infra/
│   ├── main.tf                    # Terraform resource declarations (S3, DynamoDB)
│   ├── provider.tf                # AWS provider configuration for LocalStack
│   └── outputs.tf                 # Terraform output attributes
├── .gitignore                     # Git ignore rules (filters .tfstate, venv, cache)
├── docker-compose.yml             # Container orchestration (API, Redis, LocalStack)
├── Dockerfile                     # Multi-layer Docker image build specification
└── README.md                      # Comprehensive project documentation
```

---

## 🚀 Quickstart & Local Development

### Prerequisites
* Docker & Docker Compose
* Terraform (>= 1.5.0)
* AWS CLI with LocalStack profile configured

---

### 1. Launch Services with Docker Compose

Start the FastAPI application, Redis cache, and LocalStack AWS emulator:

```bash
docker compose up -d
```

Verify that all three containers are running:
```bash
docker compose ps
```

---

### 2. Provision Emulated Cloud Infrastructure with Terraform

Initialize and apply the Terraform configuration targeting the local LocalStack instance:

```bash
cd infra
terraform init
terraform plan
terraform apply -auto-approve
cd ..
```

Verify created resources using AWS CLI:
```bash
# Verify S3 Bucket
aws --endpoint-url=http://localhost:4566 --profile localstack s3 ls

# Verify DynamoDB Table
aws --endpoint-url=http://localhost:4566 --profile localstack dynamodb list-tables
```

---

### 3. Test the Application Endpoints

**Health Check:**
```bash
curl -X GET http://localhost:8000/health
```

**Shorten a URL:**
```bash
curl -X POST http://localhost:8000/shorten \
     -H "Content-Type: application/json" \
     -d '{"url": "https://github.com/erenakg"}'
```

---

### 4. Running the Test Suite Locally

Execute the test suite inside the active application container:

```bash
docker compose exec -e PYTHONPATH=. api pytest
```

---

## 🔄 CI/CD Workflow

The automated pipeline in `.github/workflows/ci.yml` executes on every pull request and push to `main`:
* **Runner Environment:** Spawns an `ubuntu-latest` runner with an automated Redis service container.
* **Dependency Management:** Configures Python 3.11 and installs pinned dependencies.
* **Automated Testing:** Runs `pytest` with runtime environment configuration.
* **Docker Image Validation:** Builds the container image via Docker Buildx to prevent regressions in production artifacts.

---

## 📜 License

Distributed under the MIT License.