# StockMind

> Your AI-powered portfolio assistant — built with FastAPI, React, and modern developer tools.

---

## 🚀 What is StockMind?

**StockMind** is an intelligent stock portfolio manager powered by FastAPI and React. It allows users to register, log in, and securely manage their stock and crypto holdings while receiving intelligent insights and future AI assistant support.

Whether you're tracking long-term investments or building an AI trading assistant, StockMind provides a clean foundation to grow on.

---

## 🛠️ Features

✅ Secure JWT Authentication (Login, Register, Forgot Password)  
✅ Fully async FastAPI backend with SQLAlchemy  
✅ PostgreSQL or SQLite support via `async` engine  
✅ Role-based user models (UUID primary keys)  
✅ FastAPI Users integration for rapid auth  
✅ Production-ready structure with `.env` support  
✅ React + Vite frontend (coming soon)  
✅ Future AI assistant integration for insights and alerts  
✅ GitHub Actions ready (CI/CD coming soon)

---

## 🗂️ Tech Stack

| Layer     | Tech                         |
|-----------|------------------------------|
| Backend   | FastAPI, SQLAlchemy (Async), FastAPI Users |
| Frontend  | React, TypeScript, Tailwind (coming soon) |
| Database  | SQLite / PostgreSQL          |
| Auth      | JWT (access/refresh tokens)  |
| Dev Tools | Uvicorn, Alembic (optional), Pydantic |

---

## 📁 Project Structure

stockmind/
├── app/
│ ├── users/ # User model, manager, routes
│ ├── db/ # Database config + init
│ ├── main.py # FastAPI entrypoint
│ └── ... # Future portfolio endpoints
├── .env
├── requirements.txt
└── README.md



## 🔐 Authentication Endpoints

| Method | Endpoint           | Description           |
|--------|--------------------|-----------------------|
| POST   | `/auth/login`      | Login with email/password (form-data: `username`, `password`) |
| POST   | `/auth/register`   | Register a new account |
| POST   | `/auth/forgot-password` | Request a password reset |
| POST   | `/auth/reset-password`  | Reset password using token |
| GET    | `/users/me`        | Get current logged-in user |
| GET    | `/users/{id}`      | Get user by ID (if public access allowed) |

---

## 🔧 Running Locally

1. Clone the repo  
```bash
git clone https://github.com/your-username/stockmind.git
cd stockmind
Create and activate a virtual environment

bash
Copy code
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
Install dependencies

bash
Copy code
pip install -r requirements.txt
Initialize the database

bash
Copy code
python -m app.db.init_db
Run the dev server

bash
Copy code
uvicorn app.main:app --reload
🔮 Coming Soon
Portfolio tracking models (stocks, crypto, ETFs)

AI Assistant for trade alerts and insight generation

React Frontend with user dashboard

Deployment via Docker and GitHub Actions

Optional integrations: Alpaca API, Yahoo Finance, WebSockets

📄 License
MIT License. Use freely and contribute!

🙌 Acknowledgments
Built with ❤️ by Anthony Narine

Inspired by the idea that AI can empower personal finance.
