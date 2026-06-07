# Community Blood Donation API

A REST API built with **FastAPI**, **SQLAlchemy**, and **PostgreSQL**.

## Setup Instructions

### 1. Clone & Create Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Environment
Edit `.env` with your PostgreSQL credentials.

### 4. Initialize Alembic
```bash
alembic init alembic
```
Replace `alembic/env.py` with the provided file.

### 5. Run Migrations
```bash
alembic revision --autogenerate -m "initial migration"
alembic upgrade head
```

### 6. Run the Server
```bash
uvicorn app.main:app --reload
```

### 7. Open API Docs
```
http://localhost:8000/docs
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/v1/auth/register | Register user |
| POST | /api/v1/auth/login | Login |
| POST | /api/v1/donors/ | Create donor profile |
| GET | /api/v1/donors/ | List donors |
| GET | /api/v1/donors/{id} | Get donor |
| PUT | /api/v1/donors/{id} | Update donor |
| PATCH | /api/v1/donors/{id}/availability | Update availability |
| POST | /api/v1/requests/ | Create blood request |
| GET | /api/v1/requests/ | List requests |
| GET | /api/v1/requests/{id} | Get request |
| PATCH | /api/v1/requests/{id}/status | Update status |
| DELETE | /api/v1/requests/{id} | Delete request |
| GET | /api/v1/dashboard/ | Dashboard stats |
