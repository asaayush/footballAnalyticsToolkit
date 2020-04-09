# The basic target here is to read databases from the .csv files and manipulate them.

# Import statements
import csv
import numpy
import pandas

# Invoke File
countryData_file = 'CountryData.csv'
leagueData_file = 'LeagueData.csv'
matchData_file = 'MatchData.csv'

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

# Important point to note: As it turns out, the first line of the csv is the tags.
# I should remove it after writing sufficient code to handle it. UPDATE: I can do this!

# Cleaning the data to eliminate the tags
countryData = countryData.iloc[1:,:]
leagueData = leagueData.iloc[1:,:]
matchData = matchData.iloc[1:,:]

print(countryData.shape)
print(leagueData.shape)
print(matchData.shape)
