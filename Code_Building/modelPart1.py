# The goal of this script is to model multiple Machine Learning algorithms for the project.
# I need to use the cleaned data set created.
# Win Predict Data
#
# GOAL: Predict win/loss/draw.

# Import Statements
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split, validation_curve
from sklearn.neural_network import MLPClassifier
from sklearn import metrics
import pandas
import numpy as np
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
from mlxtend.plotting import plot_decision_regions
import seaborn as sn


# Import Required Database
winPredictData = pandas.read_csv('winPredictData.csv')                    # Yet to finalize
y = winPredictData.iloc[:,8]                                  # X represents all the features, y represents the actual W/L/D

X = winPredictData.iloc[:,6:8]
X1 = winPredictData.iloc[:,3]
X = pandas.concat([X,X1],axis=1)
temp = winPredictData.loc[winPredictData['7']=='W']
W_xaxis = temp['5']            # X Axis will represent home form
W_yaxis = temp['6']            # Y Axis will represent away form
temp = winPredictData.loc[winPredictData['7']=='D']
D_xaxis = temp['5']            # X Axis will represent home form
D_yaxis = temp['6']            # Y Axis will represent away form
temp = winPredictData.loc[winPredictData['7']=='L']
L_xaxis = temp['5']            # X Axis will represent home form
L_yaxis = temp['6']            # Y Axis will represent away form

# K-Nearest Neighbors
winPredictKNNModel = KNeighborsClassifier(n_neighbors=25)
# Split Data into Training and Testing
X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.3)
print(y_train)
winPredictKNNModel.fit(X_train,y_train)             # Training the model
y_predict = winPredictKNNModel.predict(X_test)      # Predicting W/L/D
# Checking accuracy
score = metrics.accuracy_score(y_test,y_predict)
print(score)


# matplot-lib
x = [X,y].values
plot_decision_regions(X,y,clf=winPredictKNNModel,legend=2)
plt.plot(W_xaxis,W_yaxis,'r+',D_xaxis,D_yaxis,'bx',L_xaxis,L_yaxis,'g*')
plt.show()


# Support Vector Machines


y = winPredictData.iloc[:,8]
X = winPredictData.iloc[:,6:8]
X1 = winPredictData.iloc[:,3]
X = pandas.concat([X,X1],axis=1)
print(X)
X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.3)
# Neural Network
winPredictNNModel = MLPClassifier(solver='adam',hidden_layer_sizes=(60,20), activation='relu', max_iter=300)
winPredictNNModel.fit(X_train,y_train)
y_predict = winPredictNNModel.predict(X_test)
score_train = metrics.accuracy_score(y_train,y_predict)
score_test = metrics.accuracy_score(y_test,y_predict)
print('Training Score = ' + str(score_train))
print('Testing Score = ' + str(score_test))
cm = confusion_matrix(y_test,y_predict)
df_cm = pandas.DataFrame(cm)
plt.figure(figsize=(10,8))
sn.heatmap(df_cm, annot=True)
plt.show()