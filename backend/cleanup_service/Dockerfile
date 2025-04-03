FROM python:3.11-slim

WORKDIR /app

COPY cleanup_service/requirements.txt .
RUN pip install -r requirements.txt --no-cache-dir

COPY cleanup_service/app/ ./app
COPY shared/ ./shared

CMD ["python", "app/main.py"]