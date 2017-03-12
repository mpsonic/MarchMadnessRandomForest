import csv
from loadTeamData import loadReverseTeamLookup

columns = {
    "teamName":     {"type": "str",     "idx":  0},
    "region":       {"type": "str",     "idx":  1},
    "winPct":       {"type": "float",   "idx":  3},
    "rating":       {"type": "float",   "idx":  6},
    "power":        {"type": "float",   "idx":  8},
    "offense":      {"type": "float",   "idx":  10},
    "defense":      {"type": "float",   "idx":  12},
    "hfa":          {"type": "float",   "idx":  13},
    "sos":          {"type": "float",   "idx":  15}
}

def loadRatingData(season):
    ratings = {}
    teamIds = loadReverseTeamLookup()
    fileName = "data/ratings/massey-ratings-%s.tsv" % season
    with open(fileName) as tsv:
        ratingFile = csv.reader(tsv, delimiter="\t")
        ratingFile.next()
        for line in ratingFile:
            if len(line) >= 17:
                teamRatings = {}
                for key, desc in columns.iteritems():
                    if desc["type"] == "float":
                        teamRatings[key] = float(line[desc["idx"]])
                    else:
                        teamRatings[key] = line[desc["idx"]]
                name = teamRatings["teamName"]
                if name in teamIds:
                    teamId = teamIds[teamRatings["teamName"]]
                    ratings[teamId] = teamRatings
    return ratings

if __name__ == "__main__":
    loadRatingData(2017)
