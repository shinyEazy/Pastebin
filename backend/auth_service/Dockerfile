FROM python:3.11-slim

RUN apt-get update && apt-get install -y netcat-openbsd && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY auth_service/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY auth_service/app/ ./app
COPY shared/ ./shared

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]