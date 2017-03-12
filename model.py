from loadTeamData import loadTeamData, loadReverseTeamLookup
from loadTourneyData import loadTourneyData
from loadRatingData import loadRatingData
from sklearn.ensemble import RandomForestClassifier
import random
import numpy as np

teams = loadTeamData()
teamIds = loadReverseTeamLookup()
tourneyResults = loadTourneyData()
# for key in tourneyResults:
#     print key

ratings = {}
for i in range(2013, 2017):
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

def trainForest(season, ntrees):
    data = prepareTrainingData(season)
    randomForest = RandomForestClassifier(n_estimators=ntrees, n_jobs=2)
    randomForest.fit(data["features"], data["targets"])
    return { "forest":randomForest, "data": data }

def testForest(rfModel, season):
    data = prepareTrainingData(season)
    return rfModel.score(data["features"], data["targets"])


def buildModel(ntrees):
    print ("building model...")
    forests = []
    for season in range(2013, 2016):
        print season
        if season != 2017:
            trainResult = trainForest(season, ntrees)
            forest = {"season": season, "forest": trainResult["forest"], "data": trainResult["data"]}
            forests.append(forest)
    return Model(forests)


class Model:
    def __init__(self, randomForestArray):
        self.forests = randomForestArray

    def predict(self, season, team1, team2):
        teamid1 = teamIds[team1]
        teamid2 = teamIds[team2]
        X = np.asarray(compareTeamStats(season, teamid1, teamid2)).reshape(1,-1)
        s = 0
        count = 0
        for forest in self.forests:
            if forest["season"] != season:
                s += forest["forest"].predict_proba(X)[0][1]
                count += 1
        return s/count

    def validate(self):
        t = 0
        for forest1 in self.forests:
            season1 = forest1["season"]
            s = 0
            c = 0
            for forest2 in self.forests:
                if season1 != forest2["season"]:
                    season2Data = forest2["data"];
                    s += forest1["forest"].score(season2Data["features"], season2Data["targets"])
                    c += 1
            print ("Validating season %s: %f" % (season1, s/c))
            t += s/c
        return t/len(self.forests)


# if __name__ == "__main__":
#     print "building model"
#     nTreesTests = [10, 25, 50, 100, 200, 400, 800]
#     bestModel = { "score": 0, "nTrees": 0, "model": None}
#     for nTrees in nTreesTests:
#         model = buildModel(nTrees)
#         modelScore = model.validate()
#         if bestModel["score"] < modelScore:
#             bestModel = {"score": modelScore, "nTrees": nTrees, "model": model}
#     print ("Best performing model:")
#     print ("Validation Score: %s" % bestModel["score"])
#     print ("NTrees: %d" % bestModel["nTrees"])
