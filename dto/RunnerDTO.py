
from dataclasses import dataclass
from typing import Any

from utils import DatabaseUtils


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

    def avg_points(self) -> float:
        return self.points_overall / self.run_count()

    def run_count(self) -> int:
        return len(DatabaseUtils.get_all_runs_from_player(self.speedrun_username))

    def highest_points(self) -> str:
        points = {'Glitchless': self.points_glitchless, 'Out of Bounds': self.points_oob, 'Inbounds': self.points_inbounds}
        s_points = sorted(points.items(), key=lambda item: item[1], reverse=True)
        return f'{s_points[0][0]}'
