# Django REST API — Task Manager

![CI](https://github.com/razwanislamrifat-source/django-rest-taskmanager/actions/workflows/ci.yml/badge.svg)
![Python](https://img.shields.io/badge/Python-3.12-blue?style=flat-square&logo=python)
![Django](https://img.shields.io/badge/Django-5.0-green?style=flat-square&logo=django)
![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?style=flat-square&logo=docker)
![JWT](https://img.shields.io/badge/Auth-JWT-orange?style=flat-square)

A production-ready REST API for task management built with Django REST Framework. Features JWT authentication, per-user data isolation, status/priority filtering, and a full CI pipeline with Trivy security scanning.

## API Endpoints

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | `/api/auth/register/` | None | Create account |
| POST | `/api/auth/token/` | None | Get JWT token |
| POST | `/api/auth/token/refresh/` | None | Refresh token |
| GET | `/api/tasks/` | JWT | List my tasks |
| POST | `/api/tasks/` | JWT | Create task |
| GET | `/api/tasks/{id}/` | JWT | Get one task |
| PUT | `/api/tasks/{id}/` | JWT | Update task |
| PATCH | `/api/tasks/{id}/` | JWT | Partial update |
| DELETE | `/api/tasks/{id}/` | JWT | Delete task |

Filter tasks: `GET /api/tasks/?status=todo&priority=high`

## Local Setup

```bash
git clone https://github.com/razwanislamrifat-source/django-rest-taskmanager.git
cd django-rest-taskmanager
cp .env.example .env
docker compose up -d
```

API available at `http://localhost:8000`

## Quick Test

```bash
# Register
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"username":"razwan","password":"mypassword","email":"r@r.com"}'

# Get token
curl -X POST http://localhost:8000/api/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{"username":"razwan","password":"mypassword"}'

# Create task (use token from above)
curl -X POST http://localhost:8000/api/tasks/ \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"title":"Learn DevOps","status":"in_progress","priority":"high"}'
```

## Tech Stack

- **Backend:** Django 5.0 + Django REST Framework 3.15
- **Auth:** JWT via `djangorestframework-simplejwt`
- **Database:** PostgreSQL 15 (SQLite for tests)
- **Container:** Docker + Docker Compose
- **CI/CD:** GitHub Actions — lint → test → Trivy security scan
- **Server:** Gunicorn (production-ready config)

## Project Structure

```
├── app/
│   ├── tasks/          # Task model, views, serializers, tests
│   ├── users/          # Register endpoint
│   ├── taskmanager/    # Settings, URLs, WSGI
│   └── manage.py
├── Dockerfile          # Multi-stage, non-root user
├── docker-compose.yml
├── .env.example
└── .github/workflows/ci.yml
```
