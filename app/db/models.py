from uuid import UUID, uuid4
from typing import Optional
from datetime import datetime
from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .db import Model


class Match(Model):
    __tablename__ = 'matches'

    id: Mapped[UUID] = mapped_column(default=uuid4, primary_key=True)
    league: Mapped[str] = mapped_column(String(32), nullable=False)
    round_number: Mapped[int] = mapped_column(Integer, nullable=False)
    start_time: Mapped[datetime] = mapped_column(nullable=False)
    match_stats: Mapped[list['MatchStats']] = relationship(
        back_populates='match')

    def __repr__(self) -> str:
        return (f"Match: {self.league} {self.round_number} {self.start_time}")


class MatchStats(Model):
    __tablename__ = 'match_statistics'

    id: Mapped[UUID] = mapped_column(default=uuid4, primary_key=True)
    match_id: Mapped[int] = mapped_column(ForeignKey('matches.id'), index=True)
    team_id: Mapped[int] = mapped_column(ForeignKey('teams.id'), index=True)
    side: Mapped[str] = mapped_column(String(16), nullable=False)
    expected_goals: Mapped[float] = mapped_column(nullable=False)
    ball_procession: Mapped[int] = mapped_column(nullable=False)
    goal_attempts: Mapped[int] = mapped_column(nullable=False)
    match: Mapped['Match'] = relationship(back_populates='match_stats')
    team: Mapped['Team'] = relationship(back_populates='match_stats')
    lineups: Mapped[list['Lineup']] = relationship(
        back_populates='match_stats')

    def __repr__(self) -> str:
        return f"MatchStats {self.side} {self.expected_goals}"


class Team(Model):
    __tablename__ = 'teams'

    id: Mapped[int] = mapped_column(primary_key=True)
    team_name: Mapped[str] = mapped_column(String(48), nullable=False)
    country: Mapped[str] = mapped_column(String(36), nullable=False)
    match_stats: Mapped[list['MatchStats']] = relationship(
        back_populates='team')
    players: Mapped[list['Player']] = relationship(
        back_populates='team')

    def __repr__(self) -> str:
        return f"Team {self.id} {self.team_name} {self.country}"


class Player(Model):
    __tablename__ = 'players'

    id: Mapped[int] = mapped_column(primary_key=True)
    team_id: Mapped[int] = mapped_column(ForeignKey='teams.id')
    lineup_id: Mapped[int] = mapped_column(ForeignKey='lineups.id')
    number: Mapped[int] = mapped_column(nullable=False)
    short_name: Mapped[str] = mapped_column(String(32), nullable=False)
    first_name: Mapped[str] = mapped_column(String(32), nullable=False)
    second_name: Mapped[str] = mapped_column(String(32), nullable=False)
    birth_date: Mapped[datetime] = mapped_column(nullable=False)
    position: Mapped[str] = mapped_column(String(24), nullable=False)
    country: Mapped[str] = mapped_column(String(36), nullable=False)
    market_values: Mapped[list['MarketValue']] = relationship(
        back_populates='player')
    team: Mapped['Team'] = relationship(back_populates='players')
    lineups: Mapped[Optional['Lineup']] = relationship(
        back_populates='players')
    goals: Mapped[list['Goal']] = relationship(back_populates='player')

    def __repr__(self) -> str:
        return f"Player {self.short_name}"


class MarketValue(Model):
    __tablename__ = 'market_values'

    id: Mapped[int] = mapped_column(primary_key=True)
    player_id: Mapped[int] = mapped_column(ForeignKey='players.id', index=True)
    value: Mapped[int] = mapped_column(nullable=False)
    timestump: Mapped[datetime] = mapped_column(default=datetime.now())
    player: Mapped['Player'] = relationship(
        back_populates='market_values')

    def __repr__(self) -> str:
        return f"MarketValue for player {self.player_id} {self.value}"


class Lineup(Model):
    __tablename__ = 'lineups'

    id: Mapped[int] = mapped_column(primary_key=True)
    match_statistics_id: Mapped[int] = mapped_column(
        ForeignKey='match_statistics.id', index=True)
    lineup_status: Mapped[str] = mapped_column(String(18), nullable=False)
    players: Mapped[list['Player']] = relationship(back_populates='lineups')
    match_stats: Mapped['MatchStats'] = relationship(back_populates='lineups')


class Goal(Model):
    __tablename__ = 'goals'

    id: Mapped[int] = mapped_column(primary_key=True)
    player_id: Mapped[int] = mapped_column(ForeignKey='players.id', index=True)
    minute: Mapped[int] = mapped_column(nullable=False)
    player: Mapped['Player'] = relationship(back_populates='goals')
