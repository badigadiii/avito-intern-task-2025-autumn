class TeamMemberAlreadyHaveTeam(Exception):
    def __init__(self, user_id: str):
        self.user_id = user_id

    def __str__(self):
        return f"User already have team (user_id={self.user_id})."
