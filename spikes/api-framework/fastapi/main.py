# https://fastapi.tiangolo.com/tutorial/first-steps/

from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

app = FastAPI()

class TODO(BaseModel):
    identifier: int
    name: str
    is_completed: bool

class TODOCreate(BaseModel):
    name: str
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

@app.post("/todos")
def post_todos(todo: TODOCreate):
    identifier = todos[-1].identifier + 1
    todo = TODO(identifier= identifier, name=todo.name, is_completed=todo.is_completed)
    todos.append(todo)
    return {"message": "success"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="debug")
