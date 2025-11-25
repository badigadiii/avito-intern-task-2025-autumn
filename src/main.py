from fastapi import FastAPI
from .teams.router import router as teams_router

app = FastAPI()
app.include_router(teams_router, prefix="/teams", tags=["teams"])
