"""
Created on Wed Aug 23 00:31:56 2017

@author: JamesQuintero
"""

import csv
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


print("Reading data from csv")
#dataset = pd.read_csv('compiled_data_OECD.csv')
dataset = pd.read_csv('compiled_data_OECD_standardized_CCI.csv')
X = dataset.iloc[:, 2:].values #loads columns 2 and up
y = dataset.iloc[:, 1].values #loads column 1 as the US NBER data, which will be the output 
dates = dataset.iloc[:, 0].values




# Splitting the dataset into the Training set and Test set for cross validation
print("Splitting dataset into train and test data")
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 0)

# Feature Scaling
#scales data from about 95-105 to -3 to 3 or so
print("Scaling data")
from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)
X = sc.transform(X)



# Importing the Keras libraries and packages
import keras
from keras.models import Sequential
from keras.layers import Dense

print("Creating neural network")

# Initialising the ANN
classifier = Sequential()

# Adding the input layer and the first hidden layer
#the number of nodes in the input layer is the number of countries
#hidden layer has num_countries/2 nodes
classifier.add(Dense(input_dim = len(X[0]), units = int(len(X[0])/2), kernel_initializer = 'uniform', activation = 'relu'))

# Adding the output layer
#1 output layer node, since that'll be a percentage
classifier.add(Dense(units = 1, kernel_initializer = 'uniform', activation = 'sigmoid'))

# Compiling the ANN
classifier.compile(optimizer = 'adam', loss = 'binary_crossentropy', metrics = ['accuracy'])


# Fitting the ANN to the Training set
print("Training neural network")
classifier.fit(X_train, y_train, batch_size = 10, nb_epoch = 100)


# Predicting the Test set results
y_pred = classifier.predict(X_test)
y_pred = (y_pred > 0.5)

# Making the Confusion Matrix
from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_test, y_pred)

print("Confusion matrix: ")
print(str(cm))





#predict whether US should be going into a recession today
US_recession_pred = classifier.predict(X)


to_save=[]
for x in range(0, len(US_recession_pred)):
	row=[]
	row.append(dates[x])
	row.append(US_recession_pred[x][0])
	to_save.append(row)

with open("./US_recession_percentages.csv", 'w', newline='') as file:
	contents = csv.writer(file)
	contents.writerows(to_save)

print()
print()

if US_recession_pred[-1]>0.5:
	print("As of "+str(dates[-1])+", the United States is in a recession")
#because any percentage 1 or above is a considerable amount, be wary
elif US_recession_pred[-1]>0.01:
	print("As of "+str(dates[-1])+", the United States is most likely heading into a recession")
else:
	print("As of "+str(dates[-1])+", the United States is not in, or heading into, a recession")