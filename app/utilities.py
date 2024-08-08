from pydantic import BaseModel


class MatchData(BaseModel):
    league: str
    round_num: int
    start_time: str
    team_home: str
    team_away: str
    score_team_home: int
    score_team_away: int
