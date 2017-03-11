import csv

def loadTourneyData():
    # Fields: Season, Daynum, Wteam, Wscore, Lteam, Lscore, Wloc, Numot
    games = {}
    with open("data/TourneyCompactResults.csv") as t:
        tourneyResults = csv.reader(t, dialect='excel')
        fields = tourneyResults.next()
        for line in tourneyResults:
            game = {}
            for i in range(0, len(fields)):
                game[fields[i]] = line[i]
            season = int(game["Season"])
            if season not in games:
                games[season] = []
            games[season].append(game)
    return games
