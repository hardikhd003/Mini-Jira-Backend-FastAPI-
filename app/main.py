from app.database import engine, Base
from fastapi import FastAPI
from app.routes import user
from app import models
from app.auth import verify_token
from fastapi import Depends
from app.routes import project
from app.routes import task
from app.routes import comment

app = FastAPI()

app.include_router(comment.router)
app.include_router(task.router)
app.include_router(project.router)
app.include_router(user.router)
Base.metadata.create_all(bind=engine)

@app.get("/")
def home():
    return {"message": "Mini Jira API is running 🚀"}

@app.get("/protected")
def protected_route(current_user: str = Depends(verify_token)):
    return {"message": f"Hello {current_user}, you are authorized 🔥"}