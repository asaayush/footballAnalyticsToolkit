import pandas
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn import metrics
from sklearn.cluster import AffinityPropagation
from sklearn.cluster import AgglomerativeClustering
from sklearn.neural_network import MLPClassifier


teamData = pandas.read_csv('fifaTeamTable.csv')
winPredictData = pandas.read_csv('winPredictData.csv')

# Creating the clustering algorithm
# Agglomerative Clustering
'''tact = teamData.iloc[:,2:11]
clustering = AgglomerativeClustering(n_clusters=22).fit(tact)
label = clustering.labels_
label = pandas.Series(data = label)
print((label))
teamData = pandas.concat([teamData, label], axis=1)'''

# Affinity Propagation
tact = teamData.iloc[:,2:11]
clustering = AffinityPropagation().fit(tact)
label = clustering.labels_
label = pandas.Series(data = label)
teamData = pandas.concat([teamData, label], axis=1)

# K Means Clustering
'''tact = teamData.iloc[:,2:11]
clustering = KMeans(n_clusters=35,max_iter=500).fit(tact)
label = clustering.labels_
label = pandas.Series(data = label)
teamData = pandas.concat([teamData, label], axis=1)'''

winPredictData = winPredictData.loc[(winPredictData['1'] == '2013/2014') |
                                    (winPredictData['1'] == '2014/2015') |
                                    (winPredictData['1'] == '2015/2016')]

result = winPredictData.iloc[:, 8]
homeForm = winPredictData.iloc[:, 6]
awayForm = winPredictData.iloc[:, 7]
stage = winPredictData.iloc[:, 3]
initData = {'result':result,'homeForm':homeForm,'awayForm':awayForm,'stage':stage}
initData = pandas.DataFrame(data=initData)

homeTeamData = pandas.DataFrame(data=[], dtype=object)
awayTeamData = pandas.DataFrame(data=[], dtype=object)
playStyles = pandas.DataFrame(data=[], dtype=object)
size = winPredictData.shape[0]

k = pandas.Series(data=[0,0,0,0,0,0,0,0,0]);   l = pandas.Series(data = [999, 999])
initData.reset_index(inplace=True);  initData = initData.iloc[:,1:]

for index in range(0,size):
    homeTeam = winPredictData.iloc[index, :]['3']
    awayTeam = winPredictData.iloc[index, :]['4']
    homeTemp = (teamData.loc[teamData['team_api_id'] == homeTeam]).iloc[:,2:11]
    awayTemp = (teamData.loc[teamData['team_api_id'] == awayTeam]).iloc[:,2:11]
    homePS   = ((teamData.loc[teamData['team_api_id'] == homeTeam]).iloc[:,11]).to_numpy()
    awayPS   = ((teamData.loc[teamData['team_api_id'] == awayTeam]).iloc[:,11]).to_numpy()
    if homeTemp.empty | awayTemp.empty:
        homeTeamData = pandas.concat([homeTeamData, k])
        awayTeamData = pandas.concat([awayTeamData, k])
        initData.iloc[index,:] = pandas.to_numeric(initData.iloc[index, :], errors='coerce')
        playStyles = pandas.concat([playStyles, l])
    else:
        homeTeamData = pandas.concat([homeTeamData, homeTemp])
        awayTeamData = pandas.concat([awayTeamData, awayTemp])
        data = {'homePS': int(homePS), 'awayPS': int(awayPS)}
        tempPS = pandas.DataFrame(data=data,index=[0])
        playStyles = pandas.concat([playStyles, tempPS])

homeTeamData.reset_index(inplace=True);  awayTeamData.reset_index(inplace=True)
homeTeamData = homeTeamData.iloc[:,2:];  awayTeamData = awayTeamData.iloc[:,2:]
playStyles.reset_index(inplace=True);    playStyles = playStyles.iloc[:,2:]
homeTeamData = homeTeamData.dropna();    awayTeamData = awayTeamData.dropna()
initData = initData.dropna();            playStyles = playStyles.dropna()
initData.reset_index(inplace=True);      initData = initData.iloc[:,1:]
homeTeamData.reset_index(inplace=True);  awayTeamData.reset_index(inplace=True)
homeTeamData = homeTeamData.iloc[:,1:];  awayTeamData = awayTeamData.iloc[:,1:]
playStyles.reset_index(inplace=True);    playStyles = playStyles.iloc[:,1:]
taskData = pandas.concat([initData,homeTeamData,awayTeamData,playStyles],axis=1)
# X.to_csv('task2_master.csv')
y = taskData.iloc[:,0]

# X = taskData.iloc[:,5:23]       # 50.468 (51 neighbors)
# X = taskData.iloc[:,2:23]     # 63.85  (82 neighbors)
# X = taskData.iloc[:,1:4]      # 78.44 (40 neighbors)
# X = taskData.iloc[:,2:23]
X = taskData.iloc[:,[1,2,3,22,23]]            # 47.8 with Agglomerative
print(X)
score = []

X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.3)
# KNN Model
for k in range(1, 100):
    playStyleKNNModel = KNeighborsClassifier(n_neighbors=k)
    playStyleKNNModel.fit(X_train,y_train)             # Training the model
    y_predict = playStyleKNNModel.predict(X_test)      # Predicting W/L/D
    score.append(metrics.accuracy_score(y_test,y_predict))   # Checking accuracy
    print('For '+str(k)+' nearest neighbors: '+str((score[k-1])*100))
print(max(score)*100)

# Neural Net
winPredictNNModel = MLPClassifier(solver='adam', hidden_layer_sizes=(64, 16, 4, ), activation='relu', max_iter=1000)
winPredictNNModel.fit(X_train, y_train)
y_predict = winPredictNNModel.predict(X_test)
score = metrics.accuracy_score(y_test, y_predict)

print('Neural net accuracy = ' + str(score*100))