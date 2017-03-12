import Bracket
import config as conf
import model as Model
from loadTeamData import loadTeamData

def runTournamentBracket(model=None):
    year = conf.year
    if model is None:
        model = Model.buildModel(200);

    # print ("Running Tournament")
    west = Bracket.runbracket(year, conf.teams['west'], model)
    east = Bracket.runbracket(year, conf.teams['east'], model)
    south = Bracket.runbracket(year, conf.teams['south'], model)
    midwest = Bracket.runbracket(year, conf.teams['midwest'], model)
    final4teams = [west[4][0], east[4][0], south[4][0], midwest[4][0]]
    final4 = Bracket.runbracket(year, final4teams, model)
    champion = final4[2][0]
    return {
        'year': 2016,
        'west': west,
        'east': east,
        'south': south,
        'midwest': midwest,
        'final4': final4,
        'champion': champion
    }

def calculatePredictionStats(iterations, numModels):
    # find list of most likely final 4 (for each region), most likely champion
    westCounts = {}
    eastCounts = {}
    southCounts = {}
    midwestCounts = {}
    championCounts = {}
    itPerModel = iterations / numModels
    teams = loadTeamData()
    for m in range(0, numModels):
        model = Model.buildModel(1000)
        for i in range(0, itPerModel):
            # print ("Running Tournament %d" % (i + 1))
            results = runTournamentBracket(model)
            westChamp = results['west'][4][0]
            eastChamp = results['east'][4][0]
            southChamp = results['south'][4][0]
            midwestChamp = results['midwest'][4][0]
            champ = results['champion']
            if westChamp not in westCounts:
                westCounts[westChamp] = 1
            else:
                westCounts[westChamp] += 1
            if eastChamp not in eastCounts:
                eastCounts[eastChamp] = 1
            else:
                eastCounts[eastChamp] += 1
            if southChamp not in southCounts:
                southCounts[southChamp] = 1
            else:
                southCounts[southChamp] += 1
            if midwestChamp not in midwestCounts:
                midwestCounts[midwestChamp] = 1
            else:
                midwestCounts[midwestChamp] += 1
            if champ not in championCounts:
                championCounts[champ] = 1
            else:
                championCounts[champ] += 1

    westProbs = [{'team': key, 'prob': westCounts[key]/float(iterations)} for key in westCounts]
    eastProbs = [{'team': key, 'prob': eastCounts[key]/float(iterations)} for key in eastCounts]
    southProbs = [{'team': key, 'prob': southCounts[key]/float(iterations)} for key in southCounts]
    midwestProbs = [{'team': key, 'prob': midwestCounts[key]/float(iterations)} for key in midwestCounts]
    champProbs = [{'team': key, 'prob': championCounts[key]/float(iterations)} for key in championCounts]

    printTeamProbs("West Champion Probabilities", westProbs)
    printTeamProbs("East Champion Probabilities", eastProbs)
    printTeamProbs("South Champion Probabilities", southProbs)
    printTeamProbs("Midwest Champion Probabilities", midwestProbs)
    printTeamProbs("Champion Probabilities", champProbs)

def printTeamProbs(title, probs):
    def getKey(prob):
        return prob['prob']
    sortedProbs = sorted(probs, key=getKey, reverse=True)

    print(title)
    for data in sortedProbs:
        print ("%s: %f" % (data['team'], data['prob']))
    print "\n"

def makeRandomBracket(nModelTrees):
    model = Model.buildModel(nModelTrees)
    results = runTournamentBracket(model)
    printTournamentBracket(results)

def printTournamentBracket(bracket):
    print "West:"
    print Bracket.bracket_to_string(bracket['west'])
    print "East:"
    print Bracket.bracket_to_string(bracket['east'])
    print "South:"
    print Bracket.bracket_to_string(bracket['south'])
    print "Midwest:"
    print Bracket.bracket_to_string(bracket['midwest'])
    print "Final4:"
    print Bracket.bracket_to_string(bracket['final4'])
