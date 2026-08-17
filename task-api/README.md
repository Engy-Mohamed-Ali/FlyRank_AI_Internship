# Task API

A small CRUD API built with Python and FastAPI as part of the FlyRank Internship Backend Track – Week 2 Assignment A1.

The API manages a simple in-memory to-do list and supports the four CRUD operations:

- Create
- Read
- Update
- Delete

## Technologies

- Python 3.10+
- FastAPI
- Uvicorn

## Features

- Create new tasks
- Get all tasks
- Get a single task by ID
- Update existing tasks
- Delete tasks
- Request validation
- Proper HTTP status codes
- Interactive Swagger UI
- In-memory data storage

## Installation

Install the required packages:

```bash
pip install fastapi uvicorn
```

## Run the API

Start the server with:

```bash
uvicorn main:app
```

The API will run at:

```text
http://localhost:8000
```

Swagger UI is available at:

```text
http://localhost:8000/docs
```

## API Endpoints

| Method | Endpoint | Description | Success Status |
|---|---|---|---|
| GET | `/` | Get API information | 200 |
| GET | `/health` | Check API health | 200 |
| GET | `/tasks` | Get all tasks | 200 |
| GET | `/tasks/{task_id}` | Get a task by ID | 200 |
| POST | `/tasks` | Create a new task | 201 |
| PUT | `/tasks/{task_id}` | Update a task | 200 |
| DELETE | `/tasks/{task_id}` | Delete a task | 204 |

## Task Structure

```json
{
  "id": 1,
  "title": "Learn FastAPI",
  "done": false
}
```

## Initial Tasks

The API starts with three example tasks:

```json
[
  {
    "id": 1,
    "title": "Learn FastAPI",
    "done": false
  },
  {
    "id": 2,
    "title": "Build CRUD API",
    "done": false
  },
  {
    "id": 3,
    "title": "Publish to GitHub",
    "done": false
  }
]
```

## Create a Task

### Request

```bash
curl -i -X POST http://localhost:8000/tasks -H "Content-Type: application/json" -d "{\"title\":\"Buy milk\"}"
```

### Example Response

```text
HTTP/1.1 201 Created
content-type: application/json

{"id":4,"title":"Buy milk","done":false}
```

The server automatically assigns the next available ID and sets `done` to `false`.

## Read All Tasks

```bash
curl -i http://localhost:8000/tasks
```

Returns the complete list of tasks.

## Read One Task

```bash
curl -i http://localhost:8000/tasks/1
```

Returns the task with ID `1`.

If the task does not exist:

```text
HTTP/1.1 404 Not Found
```

Example error:

```json
{
  "error": "Task 99 not found"
}
```

## Update a Task

```bash
curl -i -X PUT http://localhost:8000/tasks/4 -H "Content-Type: application/json" -d "{\"title\":\"Buy milk and bread\",\"done\":true}"
```

Example response:

```json
{
  "id": 4,
  "title": "Buy milk and bread",
  "done": true
}
```

The update request validates the task title and the `done` value.

## Delete a Task

```bash
curl -i -X DELETE http://localhost:8000/tasks/4
```

A successful delete returns:

```text
HTTP/1.1 204 No Content
```

The response has no body.

If the task does not exist:

```text
HTTP/1.1 404 Not Found
```

## Validation

The API validates incoming request bodies.

For example, creating a task without a title:

```bash
curl -i -X POST http://localhost:8000/tasks -H "Content-Type: application/json" -d "{}"
```

returns:

```text
HTTP/1.1 400 Bad Request
```

Example error:

```json
{
  "error": "Title is required and cannot be empty"
}
```

Invalid JSON also returns `400 Bad Request`.

## HTTP Status Codes

| Status Code | Meaning |
|---|---|
| 200 | Request successful |
| 201 | Task successfully created |
| 204 | Task successfully deleted |
| 400 | Invalid request or validation error |
| 404 | Task not found |

## Swagger UI

FastAPI automatically generates interactive API documentation using Swagger UI.

Open:

```text
http://localhost:8000/docs
```

Swagger UI allows the API endpoints to be tested directly using the **Try it out** button.

The complete CRUD cycle can be tested from Swagger UI:

1. Create a task
2. Get the task
3. Update the task
4. Delete the task
5. Confirm that the task no longer exists

## Data Storage

The tasks are stored in an in-memory Python list.

There is no database in this assignment.

Because the data is stored only in memory, all newly created or updated tasks are lost when the server is restarted. The API returns to the original three example tasks after restarting.

## Project Structure

```text
task-api/
├── main.py
└── README.md
```

## Project Goal

This project was built to practice backend fundamentals including:

- HTTP methods
- REST-style API endpoints
- CRUD operations
- Request and response handling
- HTTP status codes
- Input validation
- Path parameters
- JSON
- Swagger UI
- Git and GitHub
