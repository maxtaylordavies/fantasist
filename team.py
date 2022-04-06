from typing import Dict, List, Union

from results.weekend import Weekend

# map teams to drivers
teamDriversMap = {
    "Ferrari": ["Charles Leclerc", "Carlos Sainz"],
    "Red Bull": ["Max Verstappen", "Sergio Perez"],
    "Mercedes": ["Lewis Hamilton", "George Russell"],
    "Haas": ["Kevin Magnussen", "Mick Schumacher"],
    "Alpine": ["Fernando Alonso", "Esteban Ocon"],
    "Alfa Romeo": ["Valtteri Bottas", "Zhou Guanyu"],
    "Alpha Tauri": ["Pierre Gasly", "Yuki Tsunoda"],
    "Mclaren": ["Lando Norris", "Daniel Ricciardo"],
    "Aston Martin": ["Sebastian Vettel", "Lance Stroll"],
    "Williams": ["Alex Albon", "Nicholas Latifi"],
}

# map race position to fantasy score
racePointsMap = {1: 25, 2: 18, 3: 15, 4: 12, 5: 10, 6: 8, 7: 6, 8: 4, 9: 2, 10: 1}

# driver cost map (2022-04-06)
driverCostMap = {
    "Lewis Hamilton": 30.6,
    "Max Verstappen": 30.4,
    "George Russell": 23.7,
    "Charles Leclerc": 18.7,
    "Sergio Perez": 17.7,
    "Carlos Sainz": 17.3,
    "Lando Norris": 15.4,
    "Daniel Ricciardo": 13.8,
    "Pierre Gasly": 13.3,
    "Esteban Ocon": 12.5,
    "Fernando Alonso": 12.3,
    "Sebastian Vettel": 11.5,
    "Valtteri Bottas": 9.5,
    "Lance Stroll": 9.1,
    "Yuki Tsunoda": 8.5,
    "Zhou Guanyu": 8.2,
    "Alex Albon": 7.3,
    "Nicholas Latifi": 6.8,
    "Mick Schumacher": 6.4,
    "Kevin Magnussen": 6.0,
}

# team cost map (2022-04-06)
teamCostMap = {
    "Mercedes": 34.1,
    "Red Bull": 32.4,
    "Ferrari": 25.7,
    "Mclaren": 17.6,
    "Alpine": 13.9,
    "Aston Martin": 11.1,
    "Alpha Tauri": 10.3,
    "Alfa Romeo": 8.5,
    "Williams": 6.8,
    "Haas": 6.2,
}

# helper func to get driver's teammate
def getTeammate(driver: str) -> str:
    for team in teamDriversMap:
        if driver in teamDriversMap[team]:
            return [d for d in teamDriversMap[team] if d != driver][0]


# given the positions of teammates a and b, return whether a beat b
def beatTeammate(a: Union[int, str], b: Union[int, str]) -> bool:
    if a in ("NC", "DSQ"):
        return False
    elif b in ("NC", "DSQ"):
        return True
    return a < b


class Team:
    def __init__(self, drivers: List[str], team: str, turbo: str) -> None:
        self.drivers = drivers
        self.team = team
        self.turbo = turbo

    def isValid(self) -> bool:
        return (
            sum([driverCostMap[d] for d in self.drivers]) + teamCostMap[self.team]
            <= 101.7
            and driverCostMap[self.turbo] <= 20
        )

    def evalQualiScore(self, qualiResults: Dict) -> float:
        score = 0

        def helper(driver, team=False):
            tmp, pos = 0, qualiResults[driver]
            if pos == "DSQ":
                tmp -= 10
            elif pos == "NC":
                tmp -= 5
            else:
                if pos >= 16:  # out in Q1
                    tmp += 1
                elif pos >= 11:  # out in Q2
                    tmp += 2
                else:  # out in Q3
                    tmp += 3
                if pos <= 10:  # position bonus
                    tmp += 11 - pos
                if not team and beatTeammate(pos, qualiResults[getTeammate(driver)]):
                    tmp += 2
            ans = (2 * tmp) if (driver == self.turbo and not team) else tmp
            return ans

        for driver in self.drivers:
            score += helper(driver)
        for driver in teamDriversMap[self.team]:
            score += helper(driver, team=True)

        return score

    def evalRaceScore(
        self, qualiResults: Dict, raceResults: Dict, fastestLap: str
    ) -> float:
        score = 0

        def helper(driver, team=False):
            tmp, pos = 0, raceResults[driver]
            if pos == "DSQ":
                tmp = -20
            elif pos == "NC":
                tmp = -10
            else:
                # point for finishing
                tmp += 1
                # points for positions gained / lost
                diff = 2 * (qualiResults[driver] - pos)
                tmp += diff if abs(diff) <= 10 else 10 * (diff / abs(diff))
                # points for race position
                if pos <= 10:
                    tmp += racePointsMap[pos]
                # points for fastest lap
                if driver == fastestLap:
                    tmp += 5
                # points for beating teammate
                if not team and beatTeammate(pos, raceResults[getTeammate(driver)]):
                    tmp += 3
            ans = (2 * tmp) if (driver == self.turbo and not team) else tmp
            return ans

        for driver in self.drivers:
            score += helper(driver)
        for driver in teamDriversMap[self.team]:
            score += helper(driver, team=True)

        return score

    def evalScore(self, weekend: Weekend) -> float:
        return self.evalQualiScore(weekend.quali) + self.evalRaceScore(
            weekend.quali, weekend.race, weekend.fastestLap
        )

    def toStr(self) -> str:
        return str(self.__dict__)
