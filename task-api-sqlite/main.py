import sqlite3

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel


app = FastAPI(
    title="Task API",
    version="1.0",
    description="A small CRUD API for managing tasks."
)


DB_NAME = "tasks.db"


def init_db():
    conn = sqlite3.connect(DB_NAME)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            done INTEGER NOT NULL DEFAULT 0
        )
    """)

    count = conn.execute(
        "SELECT COUNT(*) FROM tasks"
    ).fetchone()[0]

    if count == 0:
        conn.executemany(
            "INSERT INTO tasks (title, done) VALUES (?, ?)",
            [
                ("Learn FastAPI", 0),
                ("Build CRUD API", 0),
                ("Publish to GitHub", 0),
            ]
        )

    conn.commit()
    conn.close()


init_db()


class TaskCreate(BaseModel):
    title: str


class TaskUpdate(BaseModel):
    title: str | None = None
    done: bool | None = None


@app.get(
    "/",
    summary="API information",
    description="Returns basic information about the Task API."
)
def root():
    return {
        "name": "Task API",
        "version": "1.0",
        "endpoints": ["/tasks"]
    }


@app.get(
    "/health",
    summary="Health check",
    description="Checks whether the API is running."
)
def health():
    return {"status": "ok"}


@app.get(
    "/tasks",
    summary="List all tasks",
    description="Returns all tasks."
)
def get_tasks():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row

    rows = conn.execute(
        "SELECT * FROM tasks"
    ).fetchall()

    conn.close()

    return [dict(row) for row in rows]


@app.get(
    "/tasks/{task_id}",
    summary="Get one task",
    description="Returns a task by its ID."
)
def get_task(task_id: int):
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row

    row = conn.execute(
        "SELECT * FROM tasks WHERE id = ?",
        (task_id,)
    ).fetchone()

    conn.close()

    if row is None:
        return JSONResponse(
            status_code=404,
            content={"error": "Task not found"}
        )

    task = dict(row)
    task["done"] = bool(task["done"])

    return task


@app.post(
    "/tasks",
    status_code=201,
    summary="Create a task",
    description="Creates a new task."
)
def create_task(task: TaskCreate):
    if not task.title.strip():
        return JSONResponse(
            status_code=400,
            content={"error": "Title is required and cannot be empty"}
        )

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.execute(
        "INSERT INTO tasks (title, done) VALUES (?, ?)",
        (task.title.strip(), 0)
    )

    new_id = cursor.lastrowid

    conn.commit()

    conn.close()

    return {
        "id": new_id,
        "title": task.title.strip(),
        "done": False
    }


@app.put(
    "/tasks/{task_id}",
    summary="Update a task",
    description="Updates the title and/or done status of a task."
)
def update_task(task_id: int, task: TaskUpdate):
    if task.title is None and task.done is None:
        return JSONResponse(
            status_code=400,
            content={"error": "Request body cannot be empty"}
        )

    if task.title is not None and not task.title.strip():
        return JSONResponse(
            status_code=400,
            content={"error": "Title is required and cannot be empty"}
        )

    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row

    existing_task = conn.execute(
        "SELECT * FROM tasks WHERE id = ?",
        (task_id,)
    ).fetchone()

    if existing_task is None:
        conn.close()

        return JSONResponse(
            status_code=404,
            content={"error": f"Task {task_id} not found"}
        )

    new_title = (
        task.title.strip()
        if task.title is not None
        else existing_task["title"]
    )

    new_done = (
        int(task.done)
        if task.done is not None
        else existing_task["done"]
    )

    conn.execute(
        """
        UPDATE tasks
        SET title = ?, done = ?
        WHERE id = ?
        """,
        (new_title, new_done, task_id)
    )

    conn.commit()

    updated_task = conn.execute(
        "SELECT * FROM tasks WHERE id = ?",
        (task_id,)
    ).fetchone()

    conn.close()

    result = dict(updated_task)
    result["done"] = bool(result["done"])

    return result


@app.delete(
    "/tasks/{task_id}",
    status_code=204,
    summary="Delete a task",
    description="Deletes a task by its ID."
)
def delete_task(task_id: int):
    conn = sqlite3.connect(DB_NAME)

    cursor = conn.execute(
        "DELETE FROM tasks WHERE id = ?",
        (task_id,)
    )

    if cursor.rowcount == 0:
        conn.close()

        return JSONResponse(
            status_code=404,
            content={"error": f"Task {task_id} not found"}
        )

    conn.commit()
    conn.close()

    return