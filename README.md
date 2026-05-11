# Task Management API

A secure REST API with JWT authentication, containerized with Docker and CI/CD via GitHub Actions.

## Endpoints

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | /login | No | Get JWT token |
| GET | /tasks | Yes | List all tasks |
| POST | /tasks | Yes | Create a task |
| PUT | /tasks/{id} | Yes | Update a task |
| DELETE | /tasks/{id} | Yes | Delete a task |

## Run Locally

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Run with Docker

```bash
docker build -t task-api .
docker run -p 8000:8000 task-api
```

## Run Tests

```bash
pytest tests/ -v
```

## Usage

1. Login: `POST /login` with `username=rohit` and `password=password123`
2. Use the returned token in the Authorization header: `Bearer <token>`
3. Access protected routes (tasks CRUD)

API docs available at: http://localhost:8000/docs
