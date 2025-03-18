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
pip install -r requirements.txt
python create_db.py
uvicorn app.main:app --reload --port 3001
```

### Run Load Test

```sh
cd backend
uvicorn app.main:app --host 0.0.0.0 --port 3001 --workers 4
locust -f backend/load_test/locustfile.py --host http://localhost:3001
```
