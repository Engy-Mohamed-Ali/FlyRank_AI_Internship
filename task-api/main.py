from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel


app = FastAPI(
    title="Task API",
    version="1.0",
    description="A small CRUD API for managing tasks."
)


tasks = [
    {"id": 1, "title": "Learn FastAPI", "done": False},
    {"id": 2, "title": "Build CRUD API", "done": False},
    {"id": 3, "title": "Publish to GitHub", "done": False},
]


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
    return tasks


@app.get(
    "/tasks/{task_id}",
    summary="Get one task",
    description="Returns a task by its ID."
)
def get_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task

    return JSONResponse(
        status_code=404,
        content={"error": f"Task {task_id} not found"}
    )


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

    new_id = max([t["id"] for t in tasks], default=0) + 1

    new_task = {
        "id": new_id,
        "title": task.title.strip(),
        "done": False
    }

    tasks.append(new_task)

    return new_task


@app.put(
    "/tasks/{task_id}",
    summary="Update a task",
    description="Updates the title and/or done status of a task."
)
def update_task(task_id: int, task: TaskUpdate):
    for existing_task in tasks:
        if existing_task["id"] == task_id:

            if task.title is None and task.done is None:
                return JSONResponse(
                    status_code=400,
                    content={"error": "Request body cannot be empty"}
                )

            if task.title is not None:
                if not task.title.strip():
                    return JSONResponse(
                        status_code=400,
                        content={"error": "Title is required and cannot be empty"}
                    )

                existing_task["title"] = task.title.strip()

            if task.done is not None:
                existing_task["done"] = task.done

            return existing_task

    return JSONResponse(
        status_code=404,
        content={"error": f"Task {task_id} not found"}
    )


@app.delete(
    "/tasks/{task_id}",
    status_code=204,
    summary="Delete a task",
    description="Deletes a task by its ID."
)
def delete_task(task_id: int):
    for index, task in enumerate(tasks):
        if task["id"] == task_id:
            tasks.pop(index)
            return

    return JSONResponse(
        status_code=404,
        content={"error": f"Task {task_id} not found"}
    )