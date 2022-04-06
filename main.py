import itertools

from results import bahrain, saudi
from team import Team


drivers = [
    "Charles Leclerc",
    "Carlos Sainz",
    "Max Verstappen",
    "Sergio Perez",
    "Lewis Hamilton",
    "George Russell",
    "Fernando Alonso",
    "Esteban Ocon",
    "Kevin Magnussen",
    "Mick Schumacher",
    "Valtteri Bottas",
    "Zhou Guanyu",
    "Pierre Gasly",
    "Yuki Tsunoda",
    "Lando Norris",
    "Daniel Ricciardo",
    "Sebastian Vettel",
    "Lance Stroll",
    "Alex Albon",
    "Nicholas Latifi",
]

constructors = [
    "Ferrari",
    "Red Bull",
    "Mercedes",
    "Alpine",
    "Haas",
    "Alfa Romeo",
    "Alpha Tauri",
    "Mclaren",
    "Aston Martin",
    "Williams",
]


def main():
    # generate all legal teams
    driverCombos, teams = [list(x) for x in itertools.combinations(drivers, 5)], []
    for dc in driverCombos:
        for c in constructors:
            for d in dc:
                team = Team(dc, c, d)
                if team.isValid():
                    teams.append(team)

    # evaluate all generated teams on past races
    evaluation = {team.toStr(): team.evalScore(bahrain) for team in teams}

    # rank generated teams
    ranking = sorted(list(evaluation.keys()), key=lambda k: evaluation[k], reverse=True)
    for team in ranking[:5]:
        print(f"{team}: {evaluation[team]}\n")


if __name__ == "__main__":
    main()
