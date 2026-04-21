from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas, database
from app.auth import verify_token

router = APIRouter(prefix="/comments", tags=["Comments"])


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


# 🔥 Add comment to a task
@router.post("/{task_id}")
def add_comment(
    task_id: int,
    comment: schemas.CommentCreate,
    db: Session = Depends(get_db),
    current_user: str = Depends(verify_token)
):
    user = db.query(models.User).filter(models.User.email == current_user).first()

    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    new_comment = models.Comment(
        content=comment.content,
        task_id=task_id,
        user_id=user.id
    )

    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)

    return {"message": "Comment added"}


# 🔥 Get comments for a task
@router.get("/{task_id}")
def get_comments(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: str = Depends(verify_token)
):
    comments = db.query(models.Comment).filter(models.Comment.task_id == task_id).all()
    return comments