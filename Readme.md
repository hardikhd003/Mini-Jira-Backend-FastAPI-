# 🚀 Mini Jira Backend (FastAPI)

A backend system inspired by Jira, built using FastAPI.
Supports authentication, project management, task tracking, and collaboration.

---

## 🔥 Features

* 🔐 JWT Authentication (Signup/Login)
* 📁 Project Management
* ✅ Task Management with Status (To Do, In Progress, Done)
* 👥 Assign Tasks to Users
* 💬 Comments on Tasks
* 🔒 Protected Routes (OAuth2)

---

## 🛠️ Tech Stack

* FastAPI
* SQLAlchemy
* SQLite
* JWT (python-jose)
* Pydantic

---

## ⚙️ Setup Instructions

```bash
git clone https://https://github.com/hardikhd003/Mini-Jira-Backend-FastAPI-.git
cd mini-jira-backend

python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt

uvicorn app.main:app --reload
```

---

## 📌 API Docs

Swagger UI:
http://127.0.0.1:8000/docs

---

## 🧠 Learning Outcomes

* Built secure backend with JWT authentication
* Designed relational database models
* Implemented real-world features like task assignment & comments
* Debugged production-like issues

---

## 🚀 Future Improvements

* Team collaboration (multiple users per project)
* Notifications
* Frontend (React)

---
## 🌐 Live API

https://mini-jira-backend-fastapi.onrender.com/docs