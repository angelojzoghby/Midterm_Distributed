FROM python:3.11-slim

WORKDIR /app
COPY ./distributed_scraper /app

RUN pip install --no-cache-dir fastapi uvicorn pymongo beautifulsoup4 faiss-cpu prometheus-client


EXPOSE 8000
CMD ["uvicorn", "api_service:app", "--host", "0.0.0.0", "--port", "8000"]
