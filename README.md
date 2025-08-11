# AI Inference Service

FastAPI service containerized with Docker to serve AI model predictions.
Designed for deployment on Azure with autoscaling capabilities.

## Purpose
This service will expose an API to:
- Run AI/ML model inference from a deployed model
- Integrate easily with other applications or services
- Scale automatically in cloud environments (Azure)

## Run locally
pip install -r requirements.txt
uvicorn app.main:app --reload

## Run with Docker
docker build -t ai-svc:dev .
docker run --rm -p 8000:8000 ai-svc:dev