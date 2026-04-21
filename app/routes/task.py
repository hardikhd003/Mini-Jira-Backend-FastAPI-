from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas, database
from app.auth import verify_token

router = APIRouter(prefix="/tasks", tags=["Tasks"])


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


# 🔥 Create Task
@router.post("/{project_id}")
def create_task(
    project_id: int,
    task: schemas.TaskCreate,
    db: Session = Depends(get_db),
    current_user: str = Depends(verify_token)
):
    user = db.query(models.User).filter(models.User.email == current_user).first()

    project = db.query(models.Project).filter(models.Project.id == project_id).first()

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    # Optional: ensure user owns project
    if project.owner_id != user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    new_task = models.Task(
        title=task.title,
        description=task.description,
        project_id=project_id
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return {"message": "Task created successfully"}


# 🔥 Get Tasks for a Project
@router.get("/{project_id}")
def get_tasks(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: str = Depends(verify_token)
):
    user = db.query(models.User).filter(models.User.email == current_user).first()

    project = db.query(models.Project).filter(models.Project.id == project_id).first()

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    if project.owner_id != user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    tasks = db.query(models.Task).filter(models.Task.project_id == project_id).all()

    return tasks


# 🔥 Update Task Status
@router.put("/{task_id}")
def update_task_status(
    task_id: int,
    status: str,
    db: Session = Depends(get_db),
    current_user: str = Depends(verify_token)
):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    task.status = status

    db.commit()

    return {"message": "Task status updated"}


@router.put("/assign/{task_id}")
def assign_task(
    task_id: int,
    user_id: int,
    db: Session = Depends(get_db),
    current_user: str = Depends(verify_token)
):
    # requester
    user = db.query(models.User).filter(models.User.email == current_user).first()

    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    project = db.query(models.Project).filter(models.Project.id == task.project_id).first()

    # only project owner can assign
    if project.owner_id != user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    assigned_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not assigned_user:
        raise HTTPException(status_code=404, detail="User not found")

    task.assigned_to = user_id
    db.commit()

    return {"message": "Task assigned successfully"}