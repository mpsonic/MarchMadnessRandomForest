import csv

def loadTeamData():
    teams = {}
    with open("data/Teams.csv") as t:
        for line in csv.reader(t, dialect='excel'):
            teams[line[0]] = line[1]
    return teams

def loadReverseTeamLookup():
    reverse = {}
    with open("data/Teams.csv") as t:
        for line in csv.reader(t, dialect='excel'):
            reverse[line[1]] = line[0]
    return reverse
