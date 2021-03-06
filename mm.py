import TournamentStats
import optparse
import model as Model

parser = optparse.OptionParser()
parser.add_option("-s", "--stats", dest="calcStats",
                    help="Calculate tournament outcome probabilities through"
                    " simulation (most likely final four, champion)",
                    action="store_true", default=False)
parser.add_option("-b", "--bracket", dest="makeBracket",
                    help="Simulate a tournament bracket and print results",
                    action="store_true", default=False)
parser.add_option("-w", "--winner", dest="winner",
                    help="Find a tournament bracket with the given team as champion "
                    "(team name should be in quotes if it is more than one word)."
                    " Only use this flag in conjunction with the --bracket option",
                    action="store", default=False)
parser.add_option("-p", "--predict", dest="predict",
                    help="Find the probability that one team wins over the other."
                    " Put the two team names after the flag "
                    "(team name should be in quotes if it is more than one word)",
                    action="store", type="string", nargs=2, default=False)
parser.add_option("-m", "--models", dest="nModels",
                    help="Number of random forests to create when calculating "
                    "matchup probabilities", action="store", type="int",
                    default=200)
parser.add_option("-t", "--trees", dest="nTrees",
                    help="Number of decision trees generated in each random forest",
                    action="store", type="int", default=200)
parser.add_option("--load", dest="load",
                    help="Load model matchup probabilities from file "
                    "(precalculated and saved using --save)",
                    action="store_true", default=False)
parser.add_option("--save", dest="save",
                    help="Save the calculated matchup probabilities to a file",
                    action="store_true", default=False)

options, args = parser.parse_args()

model = None
if options.load:
    model = Model.buildModel(load=True)
else:
    model = Model.buildModel(
        nForests=options.nModels,
        nTrees=options.nTrees,
        save=options.save
    )

if options.calcStats:
    TournamentStats.calculatePredictionStats(model, 100000)
elif options.makeBracket:
    if options.winner:
        TournamentStats.makeRandomBracket(model, options.winner)
    else:
        TournamentStats.makeRandomBracket(model)
elif options.predict:
    team1 = options.predict[0]
    team2 = options.predict[1]
    TournamentStats.predict(model, team1, team2)
