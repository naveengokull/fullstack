from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import date, datetime
from database import get_db
from models import Employee as EmployeeModel, Task as TaskModel, User as UserModel
from schemas import DashboardStats
from auth import get_current_user

router = APIRouter(prefix="/dashboard", tags=["dashboard"])

@router.get("/stats", response_model=DashboardStats)
def get_dashboard_stats(db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    total_employees = db.query(EmployeeModel).count()
    
    total_tasks = db.query(TaskModel).count()
    
    tasks_by_status = {}
    statuses = ["Todo", "In Progress", "Done"]
    for status in statuses:
        count = db.query(TaskModel).filter(TaskModel.status == status).count()
        tasks_by_status[status] = count
    
    tasks_by_priority = {}
    priorities = ["Low", "Medium", "High", "Urgent"]
    for priority in priorities:
        count = db.query(TaskModel).filter(TaskModel.priority == priority).count()
        tasks_by_priority[priority] = count
    
    today = date.today()
    next_week = date.fromordinal(today.toordinal() + 7)
    upcoming_due_tasks = db.query(TaskModel).filter(
        TaskModel.due_date >= today,
        TaskModel.due_date <= next_week,
        TaskModel.status != "Done"
    ).count()
    
    overdue_tasks = db.query(TaskModel).filter(
        TaskModel.due_date < today,
        TaskModel.status != "Done"
    ).count()
    
    return {
        "total_employees": total_employees,
        "total_tasks": total_tasks,
        "tasks_by_status": tasks_by_status,
        "tasks_by_priority": tasks_by_priority,
        "upcoming_due_tasks": upcoming_due_tasks,
        "overdue_tasks": overdue_tasks
    }

