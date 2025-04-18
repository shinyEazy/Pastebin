## Project Setup

### Frontend Setup

```sh
cd frontend
npm install
npm start
```

### Backend Setup

```sh
cd backend
docker-compose up --build
```

### Run Load Test

```sh
cd backend
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
locust -f loadtest/load_test/locustfile.py --host http://localhost:8000
```
