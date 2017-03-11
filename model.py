from loadTeamData import loadTeamData
from loadTourneyData import loadTourneyData
from loadRatingData import loadRatingData
from sklearn.ensemble import RandomForestClassifier
import random
import numpy as np

teams = loadTeamData()
tourneyResults = loadTourneyData()
ratings = {}
for i in range(2013, 2018):
    ratings[i] = loadRatingData(i);

def compareTeamStats(season, teamid1, teamid2):
    # print ("team1: %s, team2: %s" % (teamid1, teamid2))
    r1 = ratings[season][teamid1]
    r2 = ratings[season][teamid2]
    comparison = {
        "rating":   r1["rating"]    -   r2["rating"],
        "winPct":   r1["winPct"]    /   r2["winPct"],
        "power":    r1["power"]     -   r2["power"],
        "offense":  r1["offense"]   -   r2["offense"],
        "defense":  r1["defense"]   -   r2["defense"],
        "hfa":      r1["hfa"]       -   r2["hfa"],
        "sos":      r1["sos"]       -   r2["sos"],
        "od":       r1["offense"]   -   r2["defense"],
        "do":       r1["defense"]   -   r2["offense"]
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

def test2017data():
    r = ratings[2013]
    teamIds = []
    for teamid in r:
        teamIds.append(teamid)
    return compareTeamStats(2013, teamIds[0], teamIds[1])

def trainModel(season):
    data = prepareTrainingData(season)
    randomForest = RandomForestClassifier(n_estimators=200, n_jobs=2)
    randomForest.fit(data["features"], data["targets"])
    return randomForest

def testModel(rfModel, season):
    data = prepareTrainingData(season)
    return rfModel.score(data["features"], data["targets"])

if __name__ == "__main__":
    print "training model"
    rf = trainModel(2013)
    print testModel(rf, 2014)
    print rf.feature_importances_
    # X = test2017data()
    # X = np.asarray(X).reshape(1, -1)
    # print(rf.predict_proba(X))
