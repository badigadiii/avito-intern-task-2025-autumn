from enum import Enum


class ErrorCode(str, Enum):
    TEAM_EXISTS = "team_name already exists"
    PR_EXISTS = "PR id already exists"
    PR_MERGED = "cannot reassign on merged PR"
    NOT_ASSIGNED = "reviewer is not assigned to this PR"
    NO_CANDIDATE = "no active replacement candidate in team"
    NOT_FOUND = "resource not found"
    EMPTY_TEAM = "no team members"
