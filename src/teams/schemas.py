from pydantic import BaseModel, ConfigDict


class TeamMemberBase(BaseModel):
    user_id: str
    username: str
    is_active: bool

    model_config = ConfigDict(from_attributes=True, extra="ignore")


class TeamMember(TeamMemberBase):
    pass


class TeamMemberCreate(TeamMemberBase):
    pass


class TeamBase(BaseModel):
    team_name: str
    members: list[TeamMemberBase]


class TeamQuery(BaseModel):
    team_name: str


class TeamCreate(TeamBase):
    members: list[TeamMemberCreate]


class TeamResponse(TeamBase):
    pass
