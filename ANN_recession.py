# -*- coding: utf-8 -*-
"""
Created on Wed Aug 23 00:31:56 2017

@author: JamesQuintero
"""

#source: http://stats.oecd.org/Index.aspx?DataSetCode=MEI_CLI
#any value over 100 for a month, indicates a recession

# Artificial Neural Network

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


#dataset = pd.read_csv('compiled_data_OECD.csv')
dataset = pd.read_csv('compiled_data_OECD_standardized_CCI.csv')
X = dataset.iloc[:, 2:].values
y = dataset.iloc[:, 1].values

#scales data
#X = (X/100)

# Encoding categorical data
#from sklearn.preprocessing import LabelEncoder, OneHotEncoder
#labelencoder_X_1 = LabelEncoder()
#encodes country
#X[:, 1] = labelencoder_X_1.fit_transform(X[:, 1])
#labelencoder_X_2 = LabelEncoder()
#encodes gender
#X[:, 2] = labelencoder_X_2.fit_transform(X[:, 2])
#creates dummy variables
#onehotencoder = OneHotEncoder(categorical_features = [1])
#X = onehotencoder.fit_transform(X).toarray()
#remove dummy variable to avoid dummy variable trap
#X = X[:, 1:]

# Splitting the dataset into the Training set and Test set
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 0)

# Feature Scaling
#scales data like salary
from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)
X = sc.transform(X)



# Importing the Keras libraries and packages
import keras
from keras.models import Sequential
from keras.layers import Dense

# Initialising the ANN
classifier = Sequential()

# Adding the input layer and the first hidden layer
#11 input nodes
#6 hidden layer nodes
#init is for initializing weights
#rectifier is the activation function
classifier.add(Dense(input_dim = 39, output_dim = int(39/2), init = 'uniform', activation = 'relu'))

# Adding the second hidden layer
#6 hidden layer nodes
#rectifier is the activation function
#classifier.add(Dense(output_dim = 6, init = 'uniform', activation = 'relu'))

# Adding the output layer
#1 output layer node
#sigmoid is the activation function to give a percentage
classifier.add(Dense(output_dim = 1, init = 'uniform', activation = 'sigmoid'))

# Compiling the ANN
#optimizer is the algorithm to use to find the weights. adam is a type of stochastic gradient descent.
#loss is used for the optimizer. binary_crossentropy is used for a binary outcome. If multiple, like multiple node output, use categorical_crossentropy
#metrics is a criterion for optimizing
classifier.compile(optimizer = 'adam', loss = 'binary_crossentropy', metrics = ['accuracy'])

# Fitting the ANN to the Training set
#batch learning
classifier.fit(X_train, y_train, batch_size = 10, nb_epoch = 100)

# Part 3 - Making the predictions and evaluating the model

# Predicting the Test set results
y_pred = classifier.predict(X_test)
y_pred = (y_pred > 0.5)

# Making the Confusion Matrix
from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_test, y_pred)



#predict whether US should be going into a recession today
US_recession_pred = classifier.predict(X)
print(US_recession_pred)