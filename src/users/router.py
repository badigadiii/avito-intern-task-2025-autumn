from fastapi import APIRouter, Depends

from src.users.schemas import UserSetIsActiveSchema, UserResponse
from src.users.service import UsersService, get_users_service

router = APIRouter()


@router.post("/setIsActive")
async def set_is_active(user: UserSetIsActiveSchema, users_service: UsersService = Depends(get_users_service)) -> UserResponse:
    return await users_service.set_is_active(user)

@router.get("/getReview")
async def get_review():
    pass