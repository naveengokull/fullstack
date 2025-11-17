from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
from models import Employee, Task, User 
from routers import employee, task, auth, dashboard

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="emplyX API",
    description="A REST API for managing employees and tasks",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(employee.router)
app.include_router(task.router)
app.include_router(dashboard.router)

@app.get("/")
def root():
    return {
        "message": "emplyX API",
        "docs": "/docs",
        "version": "1.0.0"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}

