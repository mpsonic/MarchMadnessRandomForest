# Usage:
    python mm.py [options]

# Options:

    -h, --help            show help message and exit
    -s, --stats           Calculate tournament outcome probabilities through
                        simulation (most likely final four, champion)
    -b, --bracket         Simulate a tournament bracket and print results
    -w WINNER, --winner=WINNER
                        Find a tournament bracket with the given team as
                        champion (team name should be in quotes if it is more
                        than one word). Only use this flag in conjunction with
                        the --bracket option
    -p PREDICT, --predict=PREDICT
                        Find the probability that one team wins over the
                        other. Put the two team names after the flag (team name
                        should be in quotes if it is more than one word)
    -m NMODELS, --models=NMODELS
                        Number of random forests to create when calculating
                        matchup probabilities
    -t NTREES, --trees=NTREES
                        Number of decision trees generated in each random
                        forest
    --load                Load model matchup probabilities from file (precalculated
                        and saved using --save)
    --save                Save the calculated matchup probabilities to a file

# Methods:
  The idea is to use machine learning to predict the outcome of each game in the
  tournament. For training data, I decided to use
  [Massey Ratings'](http://www.masseyratings.com/cb/ncaa-d1/ratings) college
  basketball ratings from 2000 to the present. I also fetched the March Madness
  tournament outcomes since 2000 from harvitronix's
  [kaggle-march-madness-2016](https://github.com/harvitronix/kaggle-march-madness-2016)
  repository on Github.

  Using this data, the script trains many random forest classifiers to predict
  the outcomes of past tournament results. When the classifiers are completed,
  they are used to compute the pairwise matchup win probabilities for every pair
  of teams in this year's tournament. These probabilities are then used to run
  bracket simulations.


# Configuration:
  In order to reuse this code for future March Madness tournaments, you'll need
  to get the new basketball ratings from
  [Massey Ratings](http://www.masseyratings.com/cb/ncaa-d1/ratings) and change
  config.py:  Change the "year" variable to the current year and enter the correct
  team names at their respective seed positions for each bracket region. Team names
  need to match the team names found in data/Teams.csv.


# Sources/Inspirations:
  Thanks to [Massey Ratings](http://www.masseyratings.com/cb/ncaa-d1/ratings)
  for providing great team rankings! I consulted havtronix's
  [kaggle-march-madness-2016](https://github.com/harvitronix/kaggle-march-madness-2016)
  repository for some machine-learning inspiration. I also re-used some code from Daniel-B-Smith's
  [MarchMadnessMonteCarlo](https://github.com/Daniel-B-Smith/MarchMadnessMonteCarlo) project
  on Github for simulating and printing tournament brackets.


# Example Output:
### Predict the outcome of a game

    python mm.py --load -p "Iowa St" Nevada
    Iowa St wins with probability of 0.928885%

### Generate a bracket with Minnesota as the winner:

    python mm.py --load -b -w Minnesota
    East:
    Villanova
    Mt St Mary's              Vil (1)
    Wisconsin
    Virginia Tech             Vir (9)  Vil (1)
    Virginia
    UNC Wilmington            Vir (5)
    Florida
    Tennessee                 Flo (4)  Vir (5)  Vir (5)
    SMU                       SMU (6)  Bay (3)  Bay (3)  Vir (5)
    Providence
    Baylor                    Bay (3)
    New Mexico St
    South Carolina            Mar (10) Duk (2)
    Marquette
    Duke                      Duk (2)
    Troy


    Midwest:
    Kansas
    NC Central                Kan (1)
    Miami FL
    Michigan St               Mia (8)  Kan (1)
    Iowa St
    Nevada                    Iow (5)
    Purdue
    Vermont                   Ver (13) Iow (5)  Kan (1)
    Creighton                 Cre (6)  Cre (6)  Cre (6)  Kan (1)
    Rhode Island
    Oregon                    Ion (14)
    Iona
    Michigan                  Okl (10) Lou (2)
    Oklahoma St
    Louisville                Lou (2)
    Jacksonville St


    West:
    Gonzaga
    S Dakota St               Gon (1)
    Northwestern
    Vanderbilt                Van (9)  Gon (1)
    Notre Dame
    Princeton                 Not (5)
    West Virginia
    Bucknell                  Buc (13) Not (5)  Gon (1)
    Maryland                  Mar (6)  Mar (6)  St  (7)  Gon (1)
    Xavier
    Florida St                FL  (14)
    FL Gulf Coast
    St Mary's CA              St  (7)  St  (7)
    VA Commonwealth
    Arizona                   Ari (2)
    North Dakota


    South:
    North Carolina
    TX Southern               Nor (1)
    Arkansas
    Seton Hall                Set (9)  Set (9)
    Minnesota
    Tennessee                 Min (5)
    Butler
    Winthrop                  But (4)  Min (5)  Min (5)
    Cincinnati                Kan (11) UCL (3)  UCL (3)  Min (5)
    Kansas St
    UCLA                      UCL (3)
    Kent
    Dayton                    Day (7)  Ken (2)
    Wichita St
    Kentucky                  Ken (2)
    N Kentucky


    Final4:
    Gonzaga
    Virginia                  Gon (1)
    Minnesota                 Min (5)  Min (5)
    Kansas

### Generate tournament outcome statistics:

    python mm.py --load -s
    West Champion Probabilities
    Gonzaga: 0.677970
    West Virginia: 0.109880
    Arizona: 0.096870
    St Mary's CA: 0.072180
    Florida St: 0.019990
    Maryland: 0.009550
    Notre Dame: 0.008820
    Vanderbilt: 0.002840
    Xavier: 0.001000
    Northwestern: 0.000850
    VA Commonwealth: 0.000030
    Princeton: 0.000020


    East Champion Probabilities
    Villanova: 0.738100
    Baylor: 0.092810
    Florida: 0.073490
    Duke: 0.042660
    SMU: 0.034150
    Virginia: 0.017090
    Marquette: 0.000830
    Virginia Tech: 0.000590
    Wisconsin: 0.000140
    South Carolina: 0.000060
    UNC Wilmington: 0.000060
    Tennessee: 0.000020


    South Champion Probabilities
    Kentucky: 0.354020
    North Carolina: 0.298330
    UCLA: 0.233970
    Wichita St: 0.068390
    Butler: 0.027570
    Cincinnati: 0.009090
    Minnesota: 0.003810
    Kansas St: 0.002160
    Seton Hall: 0.000790
    Arkansas: 0.000780
    Winthrop: 0.000540
    Tennessee: 0.000400
    Dayton: 0.000130
    Kent: 0.000010
    N Kentucky: 0.000010


    Midwest Champion Probabilities
    Kansas: 0.788000
    Louisville: 0.049290
    Oregon: 0.043530
    Oklahoma St: 0.038890
    Iowa St: 0.034460
    Purdue: 0.032320
    Creighton: 0.007930
    Miami FL: 0.002570
    Michigan: 0.002000
    Rhode Island: 0.000550
    Michigan St: 0.000190
    Vermont: 0.000130
    Iona: 0.000080
    Jacksonville St: 0.000050
    Nevada: 0.000010


    Champion Probabilities
    Gonzaga: 0.412820
    Kansas: 0.316580
    Villanova: 0.175130
    Kentucky: 0.025050
    UCLA: 0.012740
    North Carolina: 0.011360
    Baylor: 0.006690
    Florida: 0.006640
    Arizona: 0.005810
    West Virginia: 0.004980
    St Mary's CA: 0.004510
    Oklahoma St: 0.002850
    Louisville: 0.002570
    Wichita St: 0.002380
    Duke: 0.002080
    Iowa St: 0.001720
    Oregon: 0.001590
    Purdue: 0.001500
    Virginia: 0.001030
    SMU: 0.000800
    Butler: 0.000540
    Creighton: 0.000110
    Maryland: 0.000100
    Florida St: 0.000100
    Cincinnati: 0.000080
    Notre Dame: 0.000070
    Michigan: 0.000040
    Minnesota: 0.000030
    Vanderbilt: 0.000020
    Seton Hall: 0.000020
    Miami FL: 0.000020
    Marquette: 0.000020
    Kansas St: 0.000010
    Winthrop: 0.000010
