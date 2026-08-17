from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI()


tasks = [
    {"id": 1, "title": "Learn FastAPI", "done": False},
    {"id": 2, "title": "Build CRUD API", "done": False},
    {"id": 3, "title": "Publish to GitHub", "done": False},
]


@app.get("/")
def root():
    return {
        "name": "Task API",
        "version": "1.0",
        "endpoints": ["/tasks"]
    }


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/tasks")
def get_tasks():
    return tasks


@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task

    return JSONResponse(
        status_code=404,
        content={"error": f"Task {task_id} not found"}
    )


@app.post("/tasks", status_code=201)
async def create_task(request: Request):
    try:
        data = await request.json()
    except Exception:
        return JSONResponse(
            status_code=400,
            content={"error": "Invalid JSON body"}
        )

    if not isinstance(data, dict):
        return JSONResponse(
            status_code=400,
            content={"error": "Request body must be a JSON object"}
        )

    title = data.get("title")

    if not isinstance(title, str) or not title.strip():
        return JSONResponse(
            status_code=400,
            content={"error": "Title is required and cannot be empty"}
        )

    new_id = max([task["id"] for task in tasks], default=0) + 1

    new_task = {
        "id": new_id,
        "title": title.strip(),
        "done": False
    }

    tasks.append(new_task)

    return new_task


@app.put("/tasks/{task_id}")
async def update_task(task_id: int, request: Request):
    for task in tasks:
        if task["id"] == task_id:

            try:
                data = await request.json()
            except Exception:
                return JSONResponse(
                    status_code=400,
                    content={"error": "Invalid JSON body"}
                )

            if not isinstance(data, dict):
                return JSONResponse(
                    status_code=400,
                    content={"error": "Request body must be a JSON object"}
                )

            title = data.get("title", task["title"])
            done = data.get("done", task["done"])

            if not isinstance(title, str) or not title.strip():
                return JSONResponse(
                    status_code=400,
                    content={"error": "Title is required and cannot be empty"}
                )

            if not isinstance(done, bool):
                return JSONResponse(
                    status_code=400,
                    content={"error": "Done must be true or false"}
                )

            task["title"] = title.strip()
            task["done"] = done

            return task

    return JSONResponse(
        status_code=404,
        content={"error": f"Task {task_id} not found"}
    )


@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    for index, task in enumerate(tasks):
        if task["id"] == task_id:
            tasks.pop(index)
            return

    return JSONResponse(
        status_code=404,
        content={"error": f"Task {task_id} not found"}
    )