from loadTeamData import loadTeamData, loadReverseTeamLookup
from loadTourneyData import loadTourneyData
from loadRatingData import loadRatingData
from sklearn.ensemble import RandomForestClassifier
from sklearn.externals import joblib
import random
import ast
import numpy as np
import config as conf

teams = loadTeamData()
teamIds = loadReverseTeamLookup()
tourneyResults = loadTourneyData()
# for key in tourneyResults:
#     print key

ratings = {}
for i in range(2000, 2018):
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

def prepareTrainingData(season=None):
    features = []
    targets = []
    if season is not None:
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
    else:
        for season in ratings:
            if season < 2016:
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

def trainForest(ntrees, season=None):
    data = prepareTrainingData(season=season)
    randomForest = RandomForestClassifier(n_estimators=ntrees, n_jobs=2)
    randomForest.fit(data["features"], data["targets"])
    return { "forest":randomForest, "data": data }

def testForest(rfModel, season):
    data = prepareTrainingData(season=season)
    return rfModel.score(data["features"], data["targets"])


def buildModel(nForests=20, nTrees=200, save=False, load=False):
    # print ("building model...")
    if load:
        probFile = open('data/matchProbs.txt', 'r')
        matchProbs = ast.literal_eval(probFile.read())
        return Model(matchProbs)
    if nForests is None:
        nForests = 1
    matchProbs = buildSmartMatchupProbabilities(nForests, nTrees)
    if save:
        probFile = open('data/matchProbs.txt', 'w')
        probFile.write(str(matchProbs))
    return Model(matchProbs)


class Model:
    def __init__(self, matchupProbabilities):
        self.probabilities = matchupProbabilities

    def predict(self, team1, team2):
        teamid1 = teamIds[team1]
        teamid2 = teamIds[team2]
        winPct1 = self.probabilities[(teamid1, teamid2)]
        winPct2 = 1 - self.probabilities[(teamid2, teamid1)]
        return (winPct1 + winPct2) / 2
        # X = np.asarray(compareTeamStats(season, teamid1, teamid2)).reshape(1,-1)
        # return self.forest.predict_proba(X)[0][1]


def calculateMatchupProbabilities(randomForest, season, teams=None):
    probs = {}
    features = []
    indices = []
    tournamentTeams = ratings[season]
    if teams is not None:
        tournamentTeams = teams
    for teamid1 in tournamentTeams:
        for teamid2 in tournamentTeams:
            if teamid1 != teamid2:
                comparison = compareTeamStats(season, teamid1, teamid2)
                features.append(comparison)
                indices.append((teamid1, teamid2))
    rawProbs = randomForest.predict_proba(features)
    for i in xrange(len(rawProbs)):
        probs[indices[i]] = rawProbs[i][1]
    return probs

def buildSmartMatchupProbabilities(nModels, nTrees):
    probabilities = None
    for i in range(0, nModels):
        print ("training model %d" % i)
        model = trainForest(nTrees)["forest"]
        probsi = calculateMatchupProbabilities(model, conf.year, conf.all_teamids)
        if probabilities is None:
            probabilities = probsi
        else:
            for key in probabilities:
                probabilities[key] += probsi[key]
    for key in probabilities:
        probabilities[key] /= nModels
    return probabilities


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
