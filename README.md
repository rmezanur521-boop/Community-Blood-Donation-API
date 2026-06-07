<div align="center">

# 🩸 Community Blood Donation API

A production-ready **REST API** for managing community blood donation activities —
built with **FastAPI**, **PostgreSQL**, and **Clean Architecture** principles.

[![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-green?logo=fastapi)](https://fastapi.tiangolo.com)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-blue?logo=postgresql)](https://postgresql.org)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0-red)](https://sqlalchemy.org)
[![Alembic](https://img.shields.io/badge/Alembic-1.13-orange)](https://alembic.sqlalchemy.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

</div>

---

## 📌 Overview

**Community Blood Donation API** is a backend system designed to connect
**blood donors** with **requesters** in emergency situations.
It provides a complete platform for donor registration, blood request management,
and real-time availability tracking — all secured with **JWT-based authentication**
and **role-based access control**.

---

## ✨ Features

### 🔐 Authentication & Authorization
- User Registration and Login
- JWT Token-based Authentication
- Password Hashing with Bcrypt
- Role-Based Access Control (Admin / Donor / Requester)

### 🩸 Donor Management
- Create and Update Donor Profile
- Filter Donors by Blood Group and City
- Search Donors by Name
- Toggle Availability Status
- Paginated Donor Listing

### 📋 Blood Request Management
- Create Blood Requests
- View and Filter Requests by Status
- Update Request Status (Pending / Fulfilled / Cancelled)
- Delete Blood Requests

### 📊 Admin Dashboard
- Total Registered Donors
- Currently Available Donors
- Active (Pending) Blood Requests
- Total Fulfilled Requests
- Total Registered Users

---

## 🏗️ Architecture

This project follows **Clean Architecture** principles with a clear separation of concerns:

```
Request → Router → Service → Repository → Database
```
community_blood_donation/
│
├── app/
│   ├── main.py                  # App entry point
│   ├── core/                    # Config, security, exceptions
│   ├── database/                # DB engine and session
│   ├── models/                  # SQLAlchemy ORM models
│   ├── schemas/                 # Pydantic request/response models
│   ├── repositories/            # Database query layer
│   ├── services/                # Business logic layer
│   ├── routers/                 # API endpoint definitions
│   └── dependencies/            # Auth guards and role checkers
│
├── alembic/                     # Database migrations
├── requirements.txt
├── .env
└── README.md

---

## 🛠️ Tech Stack

| Technology | Purpose |
|------------|---------|
| **Python 3.12** | Core language |
| **FastAPI** | Web framework |
| **PostgreSQL** | Relational database |
| **SQLAlchemy 2.0** | ORM |
| **Alembic** | Database migrations |
| **python-jose** | JWT token generation |
| **Passlib + Bcrypt** | Password hashing |
| **Pydantic v2** | Data validation |
| **Pydantic-Settings** | Environment config |
| **Uvicorn** | ASGI server |

---

## 🗄️ Database Schema
┌─────────────┐       ┌──────────────┐       ┌─────────────────┐
│    users    │       │    donors    │       │  blood_requests  │
├─────────────┤       ├──────────────┤       ├─────────────────┤
│ id          │──┐    │ id           │       │ id              │
│ full_name   │  └───▶│ user_id (FK) │       │ patient_name    │
│ email       │       │ blood_group  │       │ blood_group     │
│ password_   │  ┌───▶│ phone        │       │ hospital_name   │
│   hash      │  │    │ city         │       │ required_date   │
│ role        │  │    │ address      │       │ contact_number  │
│ created_at  │  │    │ last_        │       │ status          │
└─────────────┘  │    │  donation_   │       │ created_by (FK)─┘
│    │  date        │       │ created_at      │
│    │ is_available │       └─────────────────┘
│    └──────────────┘
└─── (one-to-one with users)

---

## 🌐 API Endpoints

### Authentication
| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| `POST` | `/api/v1/auth/register` | Register new user | Public |
| `POST` | `/api/v1/auth/login` | Login and get token | Public |

### Donors
| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| `POST` | `/api/v1/donors/` | Create donor profile | Donor, Admin |
| `GET` | `/api/v1/donors/` | List all donors (paginated) | All roles |
| `GET` | `/api/v1/donors/{id}` | Get donor by ID | All roles |
| `PUT` | `/api/v1/donors/{id}` | Update donor profile | Owner, Admin |
| `PATCH` | `/api/v1/donors/{id}/availability` | Toggle availability | Owner, Admin |

### Blood Requests
| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| `POST` | `/api/v1/requests/` | Create blood request | Requester, Admin |
| `GET` | `/api/v1/requests/` | List all requests | All roles |
| `GET` | `/api/v1/requests/{id}` | Get request by ID | All roles |
| `PATCH` | `/api/v1/requests/{id}/status` | Update request status | Owner, Admin |
| `DELETE` | `/api/v1/requests/{id}` | Delete request | Owner, Admin |

### Dashboard
| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| `GET` | `/api/v1/dashboard/` | Get platform statistics | Admin only |

---

## 🚀 Getting Started

### Prerequisites

- Python 3.12
- PostgreSQL 14+
- Git

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/community-blood-donation-api.git
cd community-blood-donation-api
```

### 2. Create Virtual Environment

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# Mac / Linux
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the root directory:

```env
DATABASE_URL=postgresql://postgres:yourpassword@localhost:5432/community_blood_db
SECRET_KEY=your-super-secret-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

### 5. Create PostgreSQL Database

```sql
CREATE DATABASE community_blood_db;
```

### 6. Run Database Migrations

```bash
alembic revision --autogenerate -m "initial migration"
alembic upgrade head
```

### 7. Start the Server

```bash
uvicorn app.main:app --reload
```

### 8. Explore the API

| Interface | URL |
|-----------|-----|
| **Swagger UI** | http://localhost:8000/docs |
| **ReDoc** | http://localhost:8000/redoc |
| **Health Check** | http://localhost:8000/ |

---

## 🔑 User Roles

| Role | Description |
|------|-------------|
| **Admin** | Full access — manage all donors, requests, and view dashboard |
| **Donor** | Can create/update own donor profile and view requests |
| **Requester** | Can create and manage blood requests |

---

## 🧪 Quick API Test

### Register a User
```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "full_name": "Rahim Uddin",
    "email": "rahim@example.com",
    "password": "securepassword",
    "role": "donor"
  }'
```

### Login
```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "rahim@example.com",
    "password": "securepassword"
  }'
```

### Create Donor Profile
```bash
curl -X POST http://localhost:8000/api/v1/donors/ \
  -H "Authorization: Bearer <your_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "blood_group": "B+",
    "phone": "01711234567",
    "city": "Dhaka",
    "address": "Mirpur, Dhaka"
  }'
```

---

## 👤 Author

**Mezan** — Software Engineer & Diploma Engineering Student
- 🌍 Bangladesh
- 💼 C#, ASP.NET MVC, SQL Server, Entity Framework Core, Python, FastAPI

---

## 📄 License

This project is licensed under the **MIT License**.
Feel free to use, modify, and distribute.

---

<div align="center">
Made with ❤️ and 🩸 for the community
</div>
