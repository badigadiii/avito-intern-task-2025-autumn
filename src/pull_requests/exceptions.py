class PullRequestAlreadyExists(Exception):
    def __init__(self, pull_request_id: str):
        self.pull_request_id = pull_request_id

    def __str__(self):
        return f"PR (pull_request_id={self.pull_request_id}) id already exists."
