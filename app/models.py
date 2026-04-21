from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from .database import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)

    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User")    


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    status = Column(Enum("To Do", "In Progress", "Done", name="task_status"), default="To Do")

    project_id = Column(Integer, ForeignKey("projects.id"))    
    assigned_to = Column(Integer, ForeignKey("users.id"), nullable=True)

class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String, nullable=False)

    task_id = Column(Integer, ForeignKey("tasks.id"))
    user_id = Column(Integer, ForeignKey("users.id"))    