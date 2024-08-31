from sqlalchemy.orm import Session
from models import Task
from schemas import TaskCreate

def get_tasks(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Task).offset(skip).limit(limit).all()

def get_task(db: Session, task_id: int):
    return db.query(Task).filter(Task.id == task_id).first()

def create_task(db: Session, task: TaskCreate):
    try:
        db_task = Task(title=task.title, description=task.description)
        db.add(db_task)
        db.commit()
        db.refresh(db_task)
        return db_task
    except Exception as e:
        db.rollback()
        print(f"Erro ao criar tarefa: {e}")
        raise e

def update_task(db: Session, task_id: int, task: TaskCreate):
    db_task = get_task(db, task_id)
    if db_task:
        db_task.title = task.title
        db_task.description = task.description
        db.commit()
        db.refresh(db_task)
    return db_task

def delete_task(db: Session, task_id: int):
    db_task = get_task(db, task_id)
    if db_task:
        db.delete(db_task)
        db.commit()
    return db_task
