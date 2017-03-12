import TournamentStats
import model as Model
import Bracket

# TournamentStats.calculatePredictionStats(20000)

model = Model.buildModel(50)
results = TournamentStats.runTournamentBracket(model)
TournamentStats.printTournamentBracket(results)
