from fastapi import FastAPI
from .teams.router import router as teams_router
from .users.router import router as users_router
from .pull_requests.router import router as pull_requests_router


app = FastAPI()
app.include_router(teams_router, prefix="/teams", tags=["teams"])
app.include_router(users_router, prefix="/users", tags=["users"])
app.include_router(
    pull_requests_router, prefix="/pull_requests", tags=["pull_requests"]
)
