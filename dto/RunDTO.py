from dataclasses import dataclass


@dataclass
class RunDTO:
    category: str
    speedrun_username: str
    speedrun_id: str
    level: str
    weblink: str
    video: str
    demos: str
    place: int
    points: float
    time: int
    date: int
