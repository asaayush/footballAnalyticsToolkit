# The basic target here is to read databases from the .csv files and manipulate them.

# Import statements
import csv          # not needed
import numpy        # not needed
import pandas
import re           # regular expressions

# Invoke File
countryData_file = 'CountryData.csv'
leagueData_file = 'LeagueData.csv'
matchData_file = 'MatchData.csv'
extraData_file = 'MatchData4_ExtraData_NeedsCleaning.csv'
teamData_file = 'TeamData.csv'

# We could import using any of the following strategies:
# 1. Using direct CSV readers
#       reader = csv.reader(countryData)
#       country_Data_read = list(reader)
# 2. Using numpy (preferable for just numbers)
#       country_Data_read = numpy.loadtxt(countryData, delimiter=',')
# 3. Using pandas (really useful)
tags = ['id','name']
countryData = pandas.read_csv(countryData_file, names=tags)
tags = ['id','country_id','name']
leagueData = pandas.read_csv(leagueData_file, names=tags)
tags = ['id','country_id','league_id','season','stage','date','match_api_id','home_team_api_id',
        'away_team_api_id','home_team_goal','away_team_goal']
matchData = pandas.read_csv(matchData_file, names=tags)
tags = ['goal','shoton','shotoff','foulcommit','card','cross','corner','possession']
extraData = pandas.read_csv(extraData_file, names=tags)
tags = ['id','team_api_id','team_fifa_api_id','team_long_name','team_short_name']
teamData = pandas.read_csv(teamData_file, names=tags)

# Important point to note: As it turns out, the first line of the csv is the tags.
# I should remove it after writing sufficient code to handle it. UPDATE: I can do this!

# Cleaning the data to eliminate the tags
countryData = countryData.iloc[1:,:]
leagueData = leagueData.iloc[1:,:]
matchData = matchData.iloc[1:,:]
extraData = extraData.iloc[1:,:]
teamData = teamData.iloc[1:,:]

# Just checking on the shape of the data
# print(countryData.shape)
# print(leagueData.shape)
# print(matchData.shape)
# print(extraData.shape)

extraData = extraData.dropna()
size = extraData.shape
size = size[0]
goalID = []
i = 0
while i < size:
    temp = str(extraData.iloc[i, 0])
    goalID_temp = re.findall('<id>([0-9]+)',temp)
    goalID.append(goalID_temp)
    i = i+1

# Let us now build the winPredictData.csv
# We need the following data: Form over last 'x' games. --> We need MatchData.csv
# The data has been pre-formatted in Excel to be in an order we can exploit
# In any continuous 'x' stages of the game, if 'W' is repeating (counter), good form
# I would like to ideally add a 'form score', that will act as a useful feature

yearList = matchData['season'].drop_duplicates()
teamList = teamData['team_api_id']
seasonList = yearList
countryID = countryData['id']

lastX = 3
data = {('0', '0', '0', '0', '0')}
formTable = pandas.DataFrame(data)

'''
for countryId in countryID:
    for seasonID in seasonList:
        seasonMatches = matchData.loc[(matchData['season'] == seasonID) & (matchData['country_id'] == countryId)]
        for teamID in teamList:
            form = []
            formPoints = []
            genMatches = seasonMatches.loc[(seasonMatches['home_team_api_id'] == teamID)|
                                           (seasonMatches['away_team_api_id'] == teamID)]
            stageList = genMatches['stage']
            for stage in stageList:
                #print(countryId, seasonID, teamID,stage)
                temp = genMatches.loc[(genMatches['stage'] == stage)]
                kkk = (temp.loc[temp['away_team_api_id'] == teamID]['away_team_api_id'] == teamID).empty
                homeGoal = int(temp.loc[temp['stage'] == stage, 'home_team_goal'].item())
                awayGoal = int(temp.loc[temp['stage'] == stage, 'away_team_goal'].item())
                if kkk:                                 # Home Matches
                    if homeGoal > awayGoal:
                        formPoints.append(1)                  # Home Win
                    elif homeGoal == awayGoal:
                        formPoints.append(0)                  # Home Draw
                    elif homeGoal < awayGoal:
                        formPoints.append(-1)                 # Home Loss
                else:                                   # Away Matches
                    if homeGoal < awayGoal:
                        formPoints.append(1)                  # Away Win
                    elif homeGoal == awayGoal:
                        formPoints.append(0)                  # Away Draw
                    elif homeGoal > awayGoal:
                        formPoints.append(-1)                 # Away Loss
            for i in range(0,lastX):
                form.append(0)
            for i in range(lastX,len(formPoints)):
                temp2 = 0
                for j in range(0,lastX):
                    temp2 += (lastX - j+1)*formPoints[i-j]
                form.append(temp2)
            for i in range(len(formPoints)):
                if formPoints[i] == 1:
                    formPoints[i] = 'W'
                elif formPoints[i] == 0:
                    formPoints[i] = 'D'
                else:
                    formPoints[i] = 'L'

            # We need to create a form table
            j = len(form)
            k = 0
            for i in stageList:
                d = {(seasonID, i, teamID, form[k],formPoints[k])}
                d = pandas.DataFrame(data=d)
                formTable = pandas.concat([formTable, d],ignore_index=True)
                k = k+1
                if k == j:
                    break
formTable = formTable.iloc[1:,:]
formTable.columns = ['season', 'stage', 'team_id', 'form', 'result']
formTable.to_csv('formTable.csv')
'''
formTable = pandas.read_csv('formTable.csv')
print(formTable.shape)

# Now that we have the form data, we have to finally form the data that we will be using; winPredictData.csv

# winPredictData = pandas.DataFrame({('0','0','0','0','0','0','0','0')})

# FEATURES 1:
# league, season, stage, home_team_id, away_team_id, home_form, away_form, result
# (league, season, stage, home_team_id, away_team_id) can be taken from matchData
# FEATURES 2:
# features 1 + home_team_goal, away_team_goal
i = 0
print(len(matchData))
homeTeamForm = pandas.DataFrame()
awayTeamForm = pandas.DataFrame()
matchResult = pandas.DataFrame()
for i in range(len(matchData)):
    season = matchData.iloc[i,:]['season']
    stage = matchData.iloc[i,:]['stage']
    homeTeam = matchData.iloc[i, :]['home_team_api_id']
    awayTeam = matchData.iloc[i, :]['away_team_api_id']
    temp = formTable.loc[(formTable['season']==season) & (formTable['stage']==int(stage))]
    hForm = temp.loc[temp['team_id'] == int(homeTeam)]['form']
    result = temp.loc[temp['team_id'] == int(homeTeam)]['result']
    aForm = temp.loc[temp['team_id'] == int(awayTeam)]['form']
    homeTeamForm = pandas.concat([homeTeamForm, hForm],ignore_index=True)
    awayTeamForm = pandas.concat([awayTeamForm, aForm], ignore_index=True)
    matchResult = pandas.concat([matchResult, result], ignore_index=True)

# data = {(matchData['league_id'],seasons,stages, homeTeams, awayTeams, )}
# print(homeTeamForm,awayTeamForm)


#print(matchData['league_id'], matchData['season'], matchData['stage'], matchData['home_team_api_id'],
     #             matchData['away_team_api_id'] , homeTeamForm, awayTeamForm, matchResult)
league = matchData['league_id']

winPredictData = pandas.concat([league, matchData['season'], matchData['stage'],
                                matchData['home_team_api_id'], matchData['away_team_api_id']
                                   , homeTeamForm, awayTeamForm, matchResult], axis=1,ignore_index=True)

print(winPredictData)
winPredictData.to_csv('winPredictData.csv')

