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
