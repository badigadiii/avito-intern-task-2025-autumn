from fastapi import APIRouter
from fastapi.params import Depends
from starlette import status

from .schemas import TeamResponse, TeamCreate, TeamQuery
from .service import TeamsService, get_teams_service

router = APIRouter()


@router.post("/add", status_code=status.HTTP_201_CREATED)
async def add_team(
    team: TeamCreate, teams_service: TeamsService = Depends(get_teams_service)
) -> TeamResponse:
    return await teams_service.create_team(team)


@router.get("/get", status_code=status.HTTP_200_OK)
async def get_team_members(
    team: TeamQuery, teams_service: TeamsService = Depends(get_teams_service)
) -> TeamResponse:
    return await teams_service.get_team_members(team)
