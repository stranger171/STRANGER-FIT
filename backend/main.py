from routers import users, workouts
from fastapi import FastAPI

app = FastAPI(
    title="Stranger Fit API",
    description="AI-Powered Adaptive Training Intelligence System",
    version="0.1.0",
)


@app.get("/")
def health_check():
    return {
        "status": "running",
        "message": "Stranger Fit API is alive"
    }

app.include_router(users.router)
app.include_router(workouts.router)