from loadTeamData import loadTeamData
from loadTourneyData import loadTourneyData
from loadRatingData import loadRatingData
from sklearn.ensemble import RandomForestClassifier
import random

teams = loadTeamData()
tourneyResults = loadTourneyData()
ratings = {}
for i in range(2013, 2016):
    ratings[i] = loadRatingData(i);

def compareTeamStats(season, teamid1, teamid2):
    r1 = ratings[season][teamid1]
    r2 = ratings[season][teamid2]
    comparison = {
        "power":    r1["power"]     - r2["power"],
        "offense":  r1["offense"]   - r2["offense"],
        "defense":  r1["defense"]   - r2["defense"],
        "hfa":      r1["hfa"]       - r2["hfa"],
        "sos":      r1["sos"]       - r2["sos"],
        "od":       r1["offense"]   - r2["defense"],
        "do":       r1["defense"]   - r2["offense"]
    }
    return comparison.values()

def prepareTrainingData(season):
    features = []
    targets = []
    for game in tourneyResults[season]:
        teamidW = game["Wteam"]
        teamidL = game["Lteam"]
        comparison = []
        if (random.random() > 0.5):
            comparison = compareTeamStats(season, teamidW, teamidL)
            targets.append("W")
        else:
            comparison = compareTeamStats(season, teamidL, teamidW)
            targets.append("L")
        features.append(comparison)
    return {"features": features, "targets": targets}

def trainModel():
    data = prepareTrainingData(2013)
    randomForest = RandomForestClassifier(n_estimators=10, n_jobs=2)
    randomForest.fit(data["features"], data["targets"])
    return randomForest

if __name__ == "__main__":
    print "training model"
    trainModel()
