from loadTeamData import loadReverseTeamLookup

teamIds = loadReverseTeamLookup()
teams = {}

year = 2017

# 2017 bracket teams
teams['west'] = ['Gonzaga', 'S Dakota St', 'Northwestern', 'Vanderbilt',
                    'Notre Dame', 'Princeton', 'West Virginia', 'Bucknell',
                    'Maryland', 'Xavier', 'Florida St', 'FL Gulf Coast',
                    'St Mary\'s CA', 'VA Commonwealth', 'Arizona', 'North Dakota']
teams['east'] = ['Villanova', 'Mt St Mary\'s', 'Wisconsin', 'Virginia Tech',
                    'Virginia', 'UNC Wilmington', 'Florida', 'Tennessee', # East Tennessee?
                    'SMU', 'Providence', 'Baylor', 'New Mexico St',
                    'South Carolina', 'Marquette', 'Duke', 'Troy']
teams['south'] = ['North Carolina', 'TX Southern', 'Arkansas', 'Seton Hall',
                    'Minnesota', 'Tennessee', 'Butler', 'Winthrop',     # Middle Tennessee?
                    'Cincinnati','Kansas St','UCLA','Kent',
                    'Dayton','Wichita St','Kentucky','N Kentucky']
teams['midwest'] = ['Kansas', 'NC Central', 'Miami FL', 'Michigan St',
                    'Iowa St', 'Nevada', 'Purdue', 'Vermont',
                    'Creighton', 'Rhode Island', 'Oregon', 'Iona',
                    'Michigan', 'Oklahoma St', 'Louisville', 'Jacksonville St']

# 2016 bracket teams
# teams['west'] = ['Oregon', 'Holy Cross', 'St Joseph\'s PA', 'Cincinnati',
#                 'Baylor', 'Yale', 'Duke', 'UNC Wilmington',
#                 'Texas', 'Northern Iowa', 'Texas A&M', 'WI Green Bay',
#                 'Oregon St', 'VA Commonwealth', 'Oklahoma', 'CS Bakersfield']
# teams['east'] = ['North Carolina', 'FL Gulf Coast', 'USC', 'Providence',
#                 'Indiana', 'Chattanooga', 'Kentucky', 'Stony Brook',
#                 'Notre Dame', 'Michigan', 'West Virginia', 'SF Austin',
#                 'Wisconsin', 'Pittsburgh', 'Xavier', 'Weber St']
# teams['south'] = ['Kansas', 'Austin Peay', 'Colorado', 'Connecticut',
#                 'Maryland', 'S Dakota St', 'California', 'Hawaii',
#                 'Arizona', 'Wichita St', 'Miami FL', 'Buffalo',
#                  'Iowa', 'Temple', 'Villanova', 'UNC Asheville']
# teams['midwest'] = ['Virginia', 'Hampton', 'Texas Tech', 'Butler',
#                     'Purdue', 'Ark Little Rock', 'Iowa St', 'Iona',
#                     'Seton Hall', 'Gonzaga', 'Utah', 'Fresno St',
#                     'Dayton', 'Syracuse', 'Michigan St', 'Tennessee']

all_teams = teams['west'] + teams['east'] + teams['south'] + teams['midwest']
_rankings = [1,16,8,9,5,12,4,13,6,11,3,14,7,10,2,15]
all_teamids = []
regional_rankings = {}

for region in teams:
    for (team, rank) in zip(teams[region], _rankings):
        teamId = teamIds[team]
        regional_rankings[teamId] = rank

regions = {}
for region in teams:
    for team in teams[region]:
        regions[team] = region
        teamId = teamIds[team]
        all_teamids.append(teamId)
