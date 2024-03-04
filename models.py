from pydantic import BaseModel


class PlayerInfo(BaseModel):
    player_name: str
    nationality: str
    club: str