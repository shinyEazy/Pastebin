FROM python:3.11-slim

RUN apt-get update && apt-get install -y netcat-openbsd && rm -rf /var/lib/apt/lists/*

ENV PYTHONPATH=/app

WORKDIR /app

COPY paste_service/requirements.txt .
RUN pip install -r requirements.txt --no-cache-dir

COPY paste_service/app/ ./app
COPY shared/ ./shared

# COPY paste_service/entrypoint.sh /entrypoint.sh
# RUN chmod +x /entrypoint.sh

# ENTRYPOINT ["/entrypoint.sh"]

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
