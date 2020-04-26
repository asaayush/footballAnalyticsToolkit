# The goal of this part is to classify the play styles.

import pandas
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn import metrics
from sklearn.neural_network import MLPClassifier


teamData = pandas.read_csv('fifaTeamTable.csv')
winPredictData = pandas.read_csv('winPredictData.csv')   # Yet to finalize
winPredictData = winPredictData.loc[(winPredictData['1'] == '2013/2014') |
                                    (winPredictData['1'] == '2014/2015') |
                                    (winPredictData['1'] == '2015/2016')] # (winPredictData['1'] == '2010/2011') |
                                    # (winPredictData['1'] == '2011/2012') |
                                    # (winPredictData['1'] == '2012/2013') |


homeTeamList = winPredictData['3']
awayTeamList = winPredictData['4']

y = winPredictData.iloc[:, 8]                             # X represents all the features, y represents the actual W/L/D
X = winPredictData.iloc[:,6:8]
X1 = winPredictData.iloc[:,3]


# Visualizing the Data
# plt.scatter(teamData['buildUpPlaySpeed'],teamData['chanceCreationShooting'])
# plt.show()
temp = teamData
k = []; scoreCol1 = []; scoreCol2 = []
scoreCol3 = []; scoreCol4 = []

for means in range(4, 9):
    k = [];  j = [];  missingTeams = []
    homePlayStyle = pandas.Series(data=[], dtype=object); awayPlayStyle = pandas.Series(data=[],dtype=object)
    teamData = temp
    teamData = teamData.iloc[:, 2:]
    kMM = KMeans(n_clusters=means, max_iter=800, algorithm='auto')
    kMM.fit(teamData)
    labels = list(kMM.labels_)
    playStyle = pandas.Series(data = labels, name='playStyle')
    teamData = temp
    teamData = pandas.concat([teamData,playStyle], axis=1)
    print('Number of Means = ' + str(means))
    for i in range(0, means):
        tempList = teamData.loc[teamData['playStyle'] == i]

        # print('Play Style Num  = ' + str(i))
        # print('Num of Entries  = ' + str(tempList.shape[0]))
        k.append(i)
        j.append((tempList.shape[0]))

        '''plt.subplot(4, 3, 1, xlabel='Build Up Play Speed')
        plt.scatter(tempList['buildUpPlaySpeed'], tempList['playStyle'])
        plt.subplot(4, 3, 2)
        plt.scatter(tempList['buildUpPlayDribbling'], tempList['playStyle'])
        plt.subplot(4, 3, 3)
        plt.scatter(tempList['buildUpPlayPassing'], tempList['playStyle'])
        plt.subplot(4, 3, 4)
        plt.scatter(tempList['buildUpPlayPositioningClass'], tempList['playStyle'])
        plt.subplot(4, 3, 5)
        plt.scatter(tempList['chanceCreationPassing'], tempList['playStyle'])
        plt.subplot(4, 3, 6)
        plt.scatter(tempList['chanceCreationCrossing'], tempList['playStyle'])
        plt.subplot(4, 3, 7)
        plt.scatter(tempList['chanceCreationShooting'], tempList['playStyle'])
        plt.subplot(4, 3, 8)
        plt.scatter(tempList['chanceCreationPositioningClass'], tempList['playStyle'])
        plt.subplot(4, 3, 9)
        plt.scatter(tempList['defencePressure'], tempList['playStyle'])
        plt.subplot(4, 3, 10)
        plt.scatter(tempList['defenceAggression'], tempList['playStyle'])
        plt.subplot(4, 3, 11)
        plt.scatter(tempList['defenceTeamWidth'], tempList['playStyle'])
        plt.subplot(4, 3, 12)
        plt.scatter(tempList['defenceDefenderLineClass'], tempList['playStyle'])
        plt.show()'''
    # Find the team and add the associated play style
    for homeTeam in homeTeamList:
        t = teamData.loc[teamData['team_api_id'] == homeTeam]['playStyle']
        if t.empty:
            homePlayStyle = pandas.concat([homePlayStyle, pandas.Series(data=[100])])
        homePlayStyle = pandas.concat([homePlayStyle,t])
    for awayTeam in awayTeamList:
        t = teamData.loc[teamData['team_api_id'] == awayTeam]['playStyle']
        if t.empty:
            awayPlayStyle = pandas.concat([awayPlayStyle, pandas.Series(data=[100])])
        awayPlayStyle = pandas.concat([awayPlayStyle, t])

    homePlayStyle = homePlayStyle.to_numpy();   homePlayStyle = pandas.Series(data=homePlayStyle)
    awayPlayStyle = awayPlayStyle.to_numpy();   awayPlayStyle = pandas.Series(data=awayPlayStyle)
    Xt1 = (X.iloc[:, 0]).to_numpy();        Xt1 = pandas.Series(data=Xt1)
    Xt2 = (X.iloc[:, 1]).to_numpy();        Xt2 = pandas.Series(data=Xt2)
    Xt3 = X1.to_numpy();                    Xt3 = pandas.Series(data=Xt3)
    u = y.to_numpy();                       u = pandas.Series(data=u)

    playStyle2 = pandas.concat([homePlayStyle, awayPlayStyle],axis=1)
    Xt1 = pandas.concat([Xt1, Xt2, Xt3, playStyle2, u], axis=1, ignore_index=True)    # homePlayStyle, awayPlayStyle], axis=1)
    Xt1.rename(columns={0: 'homeForm', 1: 'awayForm', 2: 'stage', 3: 'homePS', 4: 'awayPS', 5: 'result'}, inplace=True)
    Xt1 = Xt1.drop(Xt1[(Xt1.homePS == 100) | (Xt1.awayPS == 100)].index)
    Xt1.reset_index(inplace=True)

    u = Xt1['result']
    Xt1 = Xt1.iloc[:, 1:];  Xt1 = Xt1.iloc[:,0:5]
    # winMap = {'W': 1, 'D': 0, 'L': -1}
    # u = [winMap[item] for item in u]

    X_train, X_test, y_train, y_test = train_test_split(Xt1, u, test_size=0.3)
    wPWithPlayStyles = KNeighborsClassifier(n_neighbors=50)
    wPWithPlayStyles.fit(X_train, y_train)  # Training the model
    y_predict = wPWithPlayStyles.predict(X_test)  # Predicting W/L/D
    score1 = metrics.accuracy_score(y_test, y_predict)

    winPredictNNModel = MLPClassifier(solver='adam', hidden_layer_sizes=(64, 16, 4, ), activation='relu', max_iter=1000)
    winPredictNNModel.fit(X_train, y_train)
    y_predict = winPredictNNModel.predict(X_test)
    score2 = metrics.accuracy_score(y_test, y_predict)

    X_train1 = X_train.iloc[:,0:3];   X_test1 = X_test.iloc[:,0:3]
    X_train2 = X_train.iloc[:,3:5];   X_test2 = X_test.iloc[:,3:5]

    wPWithoutPlayStyles = KNeighborsClassifier(n_neighbors=50)
    wPWithoutPlayStyles.fit(X_train1, y_train)  # Training the model
    y_predict = wPWithoutPlayStyles.predict(X_test1)  # Predicting W/L/D
    score3 = metrics.accuracy_score(y_test, y_predict)

    winPredictNNModel = MLPClassifier(solver='adam', hidden_layer_sizes=(64, 16, 4, ), activation='relu', max_iter=1000)
    winPredictNNModel.fit(X_train1, y_train)
    y_predict = winPredictNNModel.predict(X_test1)
    score4 = metrics.accuracy_score(y_test, y_predict)

    print(X_train2)
    wPWithoutPlayStyles = KNeighborsClassifier(n_neighbors=50)
    wPWithoutPlayStyles.fit(X_train2, y_train)  # Training the model
    y_predict = wPWithoutPlayStyles.predict(X_test2)  # Predicting W/L/D
    score5 = metrics.accuracy_score(y_test, y_predict)

    winPredictNNModel = MLPClassifier(solver='adam', hidden_layer_sizes=(64, 16, 4,), activation='relu', max_iter=1000)
    winPredictNNModel.fit(X_train2, y_train)
    y_predict = winPredictNNModel.predict(X_test2)
    score6 = metrics.accuracy_score(y_test, y_predict)



    print('Accuracy with Play Styles      (KNN)  = ' + str(score1*100))
    print('Accuracy with Play Styles      (NN)   = ' + str(score2*100))
    print('Accuracy without Play Styles   (KNN)  = ' + str(score3*100))
    print('Accuracy without Play Styles   (NN)   = ' + str(score4*100))
    print('Accuracy with only Play Styles (KNN)  = ' + str(score5*100))
    print('Accuracy with only Play Styles (NN)   = ' + str(score6*100))

    scoreCol1.append(score1); scoreCol2.append(score2)
    scoreCol3.append(score3); scoreCol4.append(score4)

# plt.bar(k, j)

print(max(scoreCol1),max(scoreCol2),max(scoreCol3),max(scoreCol4))
#plt.subplot(1,2,1)
#plt.bar(k,scoreCol1)
#plt.subplot(1,2,2)
#plt.bar(k,scoreCol2)
#plt.show()
