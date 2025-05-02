FROM python:3.11-slim

WORKDIR /app

COPY analytics_service/requirements.txt .
RUN pip install -r requirements.txt --no-cache-dir

COPY analytics_service/app/ ./app
COPY shared/ ./shared

CMD ["python", "app/main.py"]