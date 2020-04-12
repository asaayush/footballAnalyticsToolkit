# The goal of this script is to model multiple Machine Learning algorithms for the project.
# I need to use the cleaned data set created.
# Win Predict Data
#
# GOAL: Predict win/loss/draw.

# Import Statements
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn import metrics

# Import Required Database
winPredictData = 'winPredictData.csv'                    # Yet to finalize
[X, y] = winPredictData                                  # X represents all the features, y represents the actual W/L/D

# K-Nearest Neighbors
winPredictKNNModel = KNeighborsClassifier(n_neighbors=3)
# Split Data into Training and Testing
X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.2)
winPredictKNNModel.fit(X_train,y_train)             # Training the model
y_predict = winPredictKNNModel.predict(X_test)      # Predicting W/L/D
# Checking accuracy
score = metrics.accuracy_score(y_test,y_predict)


# Support Vector Machines


# Neural Network
