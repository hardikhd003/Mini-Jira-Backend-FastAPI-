from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import models, schemas, database
from app.auth import verify_token

router = APIRouter(prefix="/projects", tags=["Projects"])


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


# 🔥 Create Project
@router.post("/")
def create_project(
    project: schemas.ProjectCreate,
    db: Session = Depends(get_db),
    current_user: str = Depends(verify_token)
):
    # get user from email
    user = db.query(models.User).filter(models.User.email == current_user).first()

    new_project = models.Project(
        title=project.title,
        description=project.description,
        owner_id=user.id
    )

    db.add(new_project)
    db.commit()
    db.refresh(new_project)

    return {"message": "Project created successfully"}


# 🔥 Get My Projects
@router.get("/")
def get_projects(
    db: Session = Depends(get_db),
    current_user: str = Depends(verify_token)
):
    user = db.query(models.User).filter(models.User.email == current_user).first()

    projects = db.query(models.Project).filter(models.Project.owner_id == user.id).all()

    return projects