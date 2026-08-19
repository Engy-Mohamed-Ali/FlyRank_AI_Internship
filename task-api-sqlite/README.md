# FlyRank Internship – Backend Track – Week 3 – Assignment A2

## Connecting CRUD API to SQLite

This project is the Week 3 Assignment A2 for the FlyRank Backend Internship.

The goal of this assignment is to take the CRUD Task API from Assignment A1 and replace the in-memory task list with a real SQLite database.

The API keeps the same CRUD endpoints and behavior, but the task data is now stored in `tasks.db`, so it survives server restarts.

---

## Technologies

- Python 3.10+
- FastAPI
- SQLite
- Python built-in `sqlite3`
- Pydantic
- Uvicorn
- Git / GitHub

---

## Project Structure

```text
task-api-sqlite/
│
├── main.py
├── tasks.db
├── .gitignore
└── README.md
```

`tasks.db` is created automatically when the application starts.

The database file is ignored by Git so that each clone can create its own local database.

---

## Why SQLite?

SQLite was chosen because:

- It is lightweight.
- It requires no separate database server.
- It requires no additional database installation.
- The whole database is stored in one file.
- The database is created automatically by the application.
- Data survives when the server restarts.
- It is simple and suitable for this small CRUD application.

The database file used by this project is:

```text
tasks.db
```

---

# Database

## Database Table

The application creates a table called `tasks` automatically if it does not already exist.

The table contains:

| Column | Type | Description |
|---|---|---|
| `id` | INTEGER | Primary key, automatically generated |
| `title` | TEXT | Task title |
| `done` | INTEGER | Completion status (`0` or `1`) |

The table is created with:

```sql
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    done INTEGER NOT NULL DEFAULT 0
);
```

---

## Seed Data

The application checks how many rows exist in the table.

If the table is empty, it inserts three example tasks:

```text
1. Learn FastAPI
2. Build CRUD API
3. Publish to GitHub
```

The seed data is inserted only when the table is empty.

This prevents the three example tasks from being duplicated every time the server starts.

---

# Installation

## 1. Create and activate a virtual environment

Windows:

```bash
python -m venv .venv
```

Activate it:

```bash
.venv\Scripts\activate
```

---

## 2. Install dependencies

```bash
pip install fastapi uvicorn pydantic
```

SQLite does not need to be installed separately because Python provides the `sqlite3` module in the standard library.

---

# Run the Application

Start the FastAPI server with:

```bash
uvicorn main:app
```

The API will be available at:

```text
http://127.0.0.1:8000
```

---

# Swagger UI

FastAPI automatically provides interactive API documentation.

Open:

```text
http://127.0.0.1:8000/docs
```

The Swagger UI can be used to test all API endpoints.

---

# API Endpoints

## GET `/`

Returns basic information about the API.

Example response:

```json
{
  "name": "Task API",
  "version": "1.0",
  "endpoints": ["/tasks"]
}
```

---

## GET `/health`

Checks whether the API is running.

Example response:

```json
{
  "status": "ok"
}
```

---

## GET `/tasks`

Returns all tasks from the SQLite database.

Example:

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

---

## GET `/tasks/{task_id}`

Returns one task by ID.

Example:

```text
GET /tasks/1
```

Response:

```json
{
  "id": 1,
  "title": "Learn FastAPI",
  "done": false
}
```

If the task does not exist:

```json
{
  "error": "Task not found"
}
```

Status code:

```text
404 Not Found
```

---

## POST `/tasks`

Creates a new task.

Request:

```json
{
  "title": "Learn SQLite"
}
```

Successful response:

```json
{
  "id": 4,
  "title": "Learn SQLite",
  "done": false
}
```

Status code:

```text
201 Created
```

An empty title returns:

```text
400 Bad Request
```

---

## PUT `/tasks/{task_id}`

Updates a task.

Example request:

```text
PUT /tasks/1
```

```json
{
  "title": "Learn FastAPI and SQLite",
  "done": true
}
```

Successful response:

```json
{
  "id": 1,
  "title": "Learn FastAPI and SQLite",
  "done": true
}
```

Possible status codes:

- `200 OK`
- `400 Bad Request`
- `404 Not Found`

---

## DELETE `/tasks/{task_id}`

Deletes a task.

Example:

```text
DELETE /tasks/1
```

Successful response:

```text
204 No Content
```

If the task does not exist:

```text
404 Not Found
```

---

# SQL Queries Used

The application uses parameterized SQL queries.

## Read all tasks

```sql
SELECT * FROM tasks;
```

## Read one task

```sql
SELECT * FROM tasks WHERE id = ?;
```

## Insert a task

```sql
INSERT INTO tasks (title, done) VALUES (?, ?);
```

## Update a task

```sql
UPDATE tasks
SET title = ?, done = ?
WHERE id = ?;
```

## Delete a task

```sql
DELETE FROM tasks WHERE id = ?;
```

The `?` placeholders are used for parameterized queries instead of inserting user input directly into SQL strings.

This helps keep database operations safe.

---

# Persistence

One of the main goals of this assignment is persistence.

With the original in-memory API, tasks disappeared when the server restarted.

With SQLite:

```text
API
 ↓
SQLite
 ↓
tasks.db
```

The task data is stored on disk.

For example:

1. Create a new task.
2. Stop the server.
3. Start the server again.
4. Request `GET /tasks`.
5. The created task is still there.

This proves that the data survives a server restart.

---

# Database Initialization

When the application starts, it:

1. Opens `tasks.db`.
2. Creates the `tasks` table if it does not exist.
3. Counts the existing rows.
4. Inserts the three example tasks only when the table is empty.
5. Commits the changes.
6. Closes the database connection.

This means a new clone of the repository can start the application without manually creating the database.

---

# Validation and Status Codes

The API keeps the expected CRUD behavior from Assignment A1.

| Situation | Status |
|---|---:|
| Successful GET | `200 OK` |
| Successful POST | `201 Created` |
| Successful DELETE | `204 No Content` |
| Invalid request body | `400 Bad Request` |
| Unknown task ID | `404 Not Found` |

Examples of invalid requests include:

- Empty task title.
- Empty PUT body.
- Unknown task ID.

---

# Parameterized Queries

The application uses parameterized SQL queries such as:

```python
conn.execute(
    "SELECT * FROM tasks WHERE id = ?",
    (task_id,)
)
```

Instead of building SQL by concatenating user input.

This separates the SQL statement from the values being supplied to it and is a safer way to work with user input.

---

# Stage Checkpoints

## Stage 0 – Create SQLite Database

- Created `tasks.db`.
- Created the `tasks` table automatically.
- Added the three seed tasks.
- Seed data is inserted only when the table is empty.
- Database survives application restarts.

## Stage 1 – Read From Database

- `GET /tasks` reads from SQLite.
- `GET /tasks/{id}` reads one row from SQLite.
- Unknown IDs return `404`.

## Stage 2 – Create New Tasks

- `POST /tasks` inserts tasks into SQLite.
- SQLite generates the task ID.
- Successful creation returns `201`.
- Invalid titles return `400`.

## Stage 3 – Update and Delete

- `PUT /tasks/{id}` updates database rows.
- `DELETE /tasks/{id}` removes database rows.
- Successful delete returns `204`.
- Unknown IDs return `404`.

## Stage 4 – Explore SQLite

Example SQL query:

```sql
SELECT * FROM tasks;
```

This query returns all rows stored in the `tasks` table.

Other useful queries:

```sql
SELECT * FROM tasks WHERE done = 1;
```

```sql
SELECT COUNT(*) FROM tasks;
```

```sql
UPDATE tasks SET done = 1;
```

```sql
DELETE FROM tasks WHERE done = 1;
```

## Stage 5 – Database Documentation

- Updated the README.
- Documented why SQLite was chosen.
- Documented the database file.
- Documented the run command.
- Documented an example SQL query.
- Documented the API endpoints and database behavior.

---

# Git Workflow

The project is developed stage by stage.

Example:

```bash
git status
```

```bash
git add main.py
```

```bash
git commit -m "Stage 1: database read endpoints"
```

```bash
git push
```

Each completed stage should have its own commit.

---

# `.gitignore`

The local SQLite database should not be committed to GitHub.

Example `.gitignore`:

```gitignore
api/
__pycache__/
*.pyc
tasks.db
.venv/
venv/
```

The important part for this assignment is:

```gitignore
tasks.db
```

This allows every clone of the project to create its own local database automatically.

---

# Clean Clone Behavior

A new clone should not require a manually created database.

After cloning the repository:

```bash
python -m venv .venv
```

```bash
.venv\Scripts\activate
```

```bash
pip install fastapi uvicorn pydantic
```

Then:

```bash
uvicorn main:app
```

The application automatically creates:

```text
tasks.db
```

It also automatically creates the `tasks` table and inserts the three example tasks.

---

# Assignment Result

The original Assignment A1 architecture was:

```text
Client → FastAPI → In-memory list
```

The new architecture is:

```text
Client → FastAPI → SQLite database
                         ↓
                     tasks.db
```

The API endpoints remain the same while the storage layer has changed from memory to persistent SQLite storage.

The main result is that task data now survives server restarts.

---

## Author

FlyRank Internship – Backend Track

Week 3 – Assignment A2
