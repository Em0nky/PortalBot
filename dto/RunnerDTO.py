from dataclasses import dataclass


@dataclass
class RunnerDTO:
    discord_id: int
    speedrun_username: str
    speedrun_id: str
    rank_overall: int
    rank_inbounds: int
    rank_oob: int
    rank_glitchless: int
    points_overall: float
    points_inbounds: float
    points_oob: float
    points_glitchless: float
