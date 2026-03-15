# https://fastapi.tiangolo.com/tutorial/first-steps/

from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
import uvicorn
import logging

logger = logging.getLogger("todo-app")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("app.log")
    ]
)

app = FastAPI()

@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"{request.method} {request.url.path}")
    response = await call_next(request)
    logger.info(f"status: {response.status_code}")
    return response

class TODO(BaseModel):
    identifier: int
    name: str
    is_completed: bool

class TODOCreate(BaseModel):
    name: str
    is_completed: bool

class TODOUpdate(BaseModel):
    is_completed: bool

todos = [
    TODO(identifier=1, name="HTTPの勉強", is_completed=False),
    TODO(identifier=2, name="クイックソートの実装", is_completed=True)
    ]

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/todos")
def get_todos():
    return todos

@app.post("/todos", status_code=201)
def post_todos(todo: TODOCreate):
    identifier = todos[-1].identifier + 1
    todo = TODO(identifier=identifier, **todo.model_dump())
    todos.append(todo)
    return {"message": "success"}

@app.patch("/todos/{identifier}")
def patch_todos(identifier: int, todo: TODOUpdate):
    for t in todos:
        if t.identifier == identifier:
            t.is_completed = todo.is_completed
            return t
    raise HTTPException(status_code=404, detail="TODO not found")

@app.delete("/todos/{identifier}")
def delete_todos(identifier: int):
    global todos
    new_todos = [t for t in todos if t.identifier != identifier]
    if len(new_todos) == len(todos):
        logger.warning(f"TODO {identifier} not found")
        raise HTTPException(status_code=404, detail="TODO not found")
    todos = new_todos
    return {"message": "success"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="debug")
