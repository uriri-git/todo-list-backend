from fastapi import FastAPI
from app.database import Base, engine
from app.routers import auth, tasks, users

Base.metadata.create_all(bind=engine)

app = FastAPI(title="TODO LIST API", version="1.0.0")

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(tasks.router)

@app.get("/", tags=["Início"])
def home():
    return {"message": "TODO LIST API no ar"}
