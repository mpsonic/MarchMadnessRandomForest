import numpy as np
import config as conf
import random
from loadTeamData import loadReverseTeamLookup
teamIds = loadReverseTeamLookup()

# Get pairs of teams. taken and adapted from Daniel-B-Smith/MarchMadnessMonteCarlo
from itertools import izip_longest
def grouper(n, iterable, fillvalue=None):
    "Collect data into fixed-length chunks or blocks"
    # grouper(3, 'ABCDEFG', 'x') --> ABC DEF Gxx
    args = [iter(iterable)] * n
    return izip_longest(fillvalue=fillvalue, *args)

def pairs(iterable):
    return grouper(2,iterable)

def playgame(team1, team2, model):
    winProb = model.predict(team1, team2)
    if (random.random() < winProb):
        return (team1, team2)
    else:
        return (team2, team1)

# taken and adapted from Daniel-B-Smith/MarchMadnessMonteCarlo on Github
def playround(teams, model):
    # print("Playing Round")
    winners = []
    losers = []
    for (team1, team2) in pairs(teams):
        winner, loser = playgame(team1, team2, model)
        winners.append(winner)
        losers.append(loser)
    return winners,losers

# taken and adapted from Daniel-B-Smith/MarchMadnessMonteCarlo on Github
def runbracket(teams, model):
    # print("Running Bracket")
    # How many rounds do we need?
    rounds = []
    nRounds = int(np.log2(len(teams)))
    winners = teams #they won to get here!
    rounds.append(winners)
    for round in xrange(nRounds):
        winners, losers = playround(winners, model)
        rounds.append(winners)
    return rounds

# taken and adapted from Daniel-B-Smith/MarchMadnessMonteCarlo on Github
def bracket_to_string(bracket):
    """ Cute version that prints out brackets for 2, 4, 8, 16, 32, 64, etc. """
    result = ''
    nrounds = len(bracket) #int(np.log2(len(teams)))
    # We'll keep the results in a big array it turns out that arrays
    # of strings have to know the max string size, otherwise things
    # will just get truncated.
    maxlen = max([len(s) for s in bracket[0]])
    dt = np.dtype([('name', np.str_, maxlen)])
    results = np.array([['' for i in xrange(len(bracket[0]))] for j in
                     xrange(nrounds)], dtype=dt['name'])
    # First round, all of the spots are filled
    results[0] = bracket[0]
    # all other rounds, we split the row in half and fill from the middle out.
    for i in xrange(1, nrounds): # we've done the 1st and last already
        # round 1 skips two, round 2 skips 4, etc.
        these_winners = bracket[i]
        # Fill top half
        idx = len(bracket[0])/2 - 1
        for team in reversed(bracket[i][:int(len(bracket[i])/2)]):
            results[i][idx] = team
            idx -= 2**i
        # Fill bottom half
        idx = len(bracket[0])/2
        for team in bracket[i][int(len(bracket[i])/2):]:
            results[i][idx] = team
            idx += 2**i

    def tr(teamName,include_rank=False,maxlen=None):
        """ Print out the team and ranking """
        result = ''
        if maxlen is not None:
            team = teamName[:maxlen]
        else:
            team = teamName
        if include_rank:
            try:
                if teamName in teamIds:
                    teamid = teamIds[teamName]
                    region = conf.regions[i]
                    result = '%s (%s)'%(team,int(conf.regional_rankings[teamid]))
            except KeyError:
                result = '%s'%(team)
        return result
    stub = '%-25s ' + ' '.join(['%-8s']*(nrounds-1))
    for i in xrange(len(bracket[0])):
        these = results[:,i]
        these = [tr(these[0], include_rank=True)] + \
            [tr(i, maxlen=3, include_rank=True) for i in these[1:]]
        result += stub % tuple(these)
        result += '\n'
    result += '\n'
    return result
