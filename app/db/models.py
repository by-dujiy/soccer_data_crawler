from .db import Model
from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column


class Match(Model):
    __tablename__ = 'matches'

    id: Mapped[int] = mapped_column(primary_key=True)
    league: Mapped[str] = mapped_column(String)
    round_num: Mapped[int] = mapped_column(Integer)
    start_time: Mapped[str] = mapped_column(String)
    team_home: Mapped[str] = mapped_column(String)
    team_away: Mapped[str] = mapped_column(String)
    score_team_home: Mapped[int] = mapped_column(Integer)
    score_team_away: Mapped[int] = mapped_column(Integer)

    def __repr__(self) -> str:
        return (f"Match: {self.start_time} {self.team_home} "
                f"{self.score_team_home}-{self.score_team_away} "
                f"{self.team_away}")
