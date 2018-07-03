## James Quintero
## https://github.com/JamesQuintero
## Created: 2017
## Modified: 2017

import csv
import os
import numpy as np
import pandas as pd



compiled_data_path = './compiled_data_OECD_standardized_CCI.csv'
data_save_path = "./US_recession_percentages.csv"
model_path = "./recession_indicator_model.h5"
train_size = 0.7 #percentage of dataset to use for training


print("Reading data from csv")
dataset = pd.read_csv(compiled_data_path)
X = dataset.iloc[:, 2:].values #loads columns 2 and up
y = dataset.iloc[:, 1].values #loads column 1 as the US NBER data, which will be the output 
dates = dataset.iloc[:, 0].values




#splits data into train and test datasets for cross validation
# X_train = X[:int(len(X)*train_size)]
# y_train = y[:int(len(y)*train_size)]
# X_test = X[int(len(X)*train_size):]
# y_test = y[int(len(y)*train_size):]
# dates_train = dates[:int(len(dates)*train_size)]
# print("End date train: "+str(dates_train[-1]))

X_train = X
y_train = y
X_test = X
y_test = y


# Feature Scaling
#scales data from about 95-105 to -3 to 3 or so
print("Scaling data")
from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)
X = sc.transform(X)

print()

# Importing the Keras libraries and packages
import keras
from keras.models import Sequential
from keras.models import load_model
from keras.layers import Dense

print()

#if model has never been trained, train it
if os.path.exists(model_path)==False:

	print("Creating neural network")

	# Initialising the ANN
	model = Sequential()
	# Adding the input layer and the first hidden layer
	#the number of nodes in the input layer is the number of countries
	#hidden layer has num_countries/2 nodes
	model.add(Dense(input_dim = len(X[0]), units = int(len(X[0])/1), kernel_initializer = 'uniform', activation = 'relu'))
	# model.add(Dense(units = int(len(X[0])/1), kernel_initializer = 'uniform', activation = 'relu'))
	# model.add(Dense(units = int(len(X[0])/1), kernel_initializer = 'uniform', activation = 'relu'))
	# Adding the output layer
	#1 output layer node, since that'll be a percentage
	model.add(Dense(units = 1, kernel_initializer = 'uniform', activation = 'sigmoid'))
	# Compiling the ANN
	model.compile(optimizer = 'adam', loss = 'binary_crossentropy', metrics = ['accuracy'])
	# Fitting the ANN to the Training set
	print("Training neural network")
	model.fit(X_train, y_train, batch_size = 5, epochs = 50)

	#saves the model for future use
	model.save(model_path)

#if model has already been trained, load it
else:
	print("Model already exists, so load it\n")

	model = load_model(model_path)




# Predicting the Test set results
y_pred = model.predict(X_test)
y_pred = (y_pred > 0.5)

# Making the Confusion Matrix
from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_test, y_pred)

print("Confusion matrix: ")
print(str(cm))





#predict whether US should be going into a recession today
US_recession_pred = model.predict(X)


to_save=[]
for x in range(0, len(US_recession_pred)):
	row=[]
	row.append(dates[x])
	row.append(US_recession_pred[x][0])
	to_save.append(row)

with open(data_save_path, 'w', newline='') as file:
	contents = csv.writer(file)
	contents.writerows(to_save)

print()
print()

print(str(US_recession_pred[-1][0]*100)+"% recession likelihood")

if US_recession_pred[-1][0]>0.5:
	print("As of "+str(dates[-1])+", the United States is in a recession")
#because any percentage 1 or above is a considerable amount, be wary
elif US_recession_pred[-1][0]>0.01:
	print("As of "+str(dates[-1])+", the United States is most likely heading into a recession")
else:
	print("As of "+str(dates[-1])+", the United States is not in, or heading into, a recession")