from typing import Dict


class Weekend:
    def __init__(self, quali: Dict, race: Dict, fastestLap: str) -> None:
        self.quali = quali
        self.race = race
        self.fastestLap = fastestLap
