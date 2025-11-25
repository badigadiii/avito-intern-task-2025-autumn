from fastapi import APIRouter, Depends
from starlette import status

from src.users.schemas import UserSetIsActiveSchema, UserResponse
from src.users.service import UsersService, get_users_service

router = APIRouter()


@router.post("/setIsActive", status_code=status.HTTP_200_OK)
async def set_is_active(user: UserSetIsActiveSchema, users_service: UsersService = Depends(get_users_service)) -> UserResponse:
    return await users_service.set_is_active(user)

@router.get("/getReview")
async def get_review():
    pass