class Matchup:
    def __init__(self, team1, team2, model):
        self.team1 = team1;
        self.team2 = team2;
        self.model = model;

    def simulate(self):
        winProb = self.model.predict(self.team1, self.team2):
        if (random.random() < winProb):
            return self.team1;
        else:
            return self.team2;
