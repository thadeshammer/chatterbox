from pydantic import BaseModel


class VoteTally(BaseModel):
    total_votes: int
    total_up_votes: int
    total_down_votes: int
