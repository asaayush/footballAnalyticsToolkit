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

# Important point to note: As it turns out, the first line of the csv is the tags.
# I should remove it after writing sufficient code to handle it. UPDATE: I can do this!

# Cleaning the data to eliminate the tags
countryData = countryData.iloc[1:,:]
leagueData = leagueData.iloc[1:,:]
matchData = matchData.iloc[1:,:]
extraData = extraData.iloc[1:,:]

# Just checking on the shape of the data
# print(countryData.shape)
# print(leagueData.shape)
# print(matchData.shape)
# print(extraData.shape)

extraData = extraData.dropna()
size = extraData.shape
size = size[0]
goalID = []
i=0
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
teamList = ['10000'] # ,'8342']
seasonList = ['2009/2010'] # ,'2010/2011']
countryID = '1'

for seasonID in seasonList:
    seasonMatches = matchData.loc[(matchData['season'] == seasonID) & (matchData['country_id'] == countryID)]
    for teamID in teamList:
        # Let us identify general form
        genMatches = seasonMatches.loc[(seasonMatches['home_team_api_id'] == teamID)|
                                       (seasonMatches['away_team_api_id'] == teamID)]
        genForm = pandas.DataFrame(genMatches['stage'])
        #print(genForm)
        counter = 1; prevState = 0; newState = 1
        lastValue = 0
        stageList = genMatches['stage']
        for stage in stageList:
            temp = genMatches.loc[(genMatches['stage'] == stage)]
            kkk = (temp.loc[temp['away_team_api_id'] == teamID]['away_team_api_id'] == teamID).empty
            homeGoal = int(temp.loc[temp['stage'] == stage, 'home_team_goal'].item())
            awayGoal = int(temp.loc[temp['stage'] == stage, 'away_team_goal'].item())
            print(stage, homeGoal,awayGoal)
            if kkk:    # Home Matches
                print('Home Match')
                if homeGoal > awayGoal:
                    print('Home Win')
                    # form[counter] = lastValue + 1*(newState+1)     # Home Win
                elif homeGoal == awayGoal:
                    print('Home Draw')
                    # form[counter] = lastValue + 0                  # Home Draw
                elif homeGoal < awayGoal:
                    print('Home Loss')
                    # form[counter] = lastValue + -1                 # Home Loss
                    #newState = 0
            else:   # Away Matches
                print('Away Match')
                if homeGoal < awayGoal:
                    print('Win')
                    #form[counter] = lastValue + 1*(newState+1)     # Away Win
                elif homeGoal == awayGoal:
                    print('Draw')
                    #form[counter] = lastValue + 0                  # Away Draw
                elif homeGoal > awayGoal:
                    print('Loss')
                    #form[counter] = lastValue + -1                 # Away Loss
            counter += 1
        #print(form)
        # if homeMatches[]
            # formCol = 1


customDF = pandas.DataFrame(matchData['league_id'])
#print(customDF)


# Let us continue
