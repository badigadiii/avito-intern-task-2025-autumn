from pydantic import BaseModel


class User(BaseModel):
    user_id: str
    username: str
    team_name: str | None
    is_active: bool

class UserSetIsActiveSchema(BaseModel):
    user_id: str
    is_active: bool

class UserResponse(User):
    pass