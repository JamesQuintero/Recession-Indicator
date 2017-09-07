## James Quintero
## https://github.com/JamesQuintero
## Created: 2017
## Modified: 2017


import os
import csv

#returns contents of csv at path
def read_from_csv(path):
		if os.path.isfile(path):
			with open(path, newline='') as file:
				contents = csv.reader(file)

				temp_list=[]
				for row in contents:
					temp_matrix=[]
					for stuff in row:
						 temp_matrix.append(stuff)
					temp_list.append(temp_matrix)

				return temp_list
		else:
			return []

#saves matrix data to path as csv
def save_to_csv(path, data):
		with open(path, 'w', newline='') as file:
			contents = csv.writer(file)
			contents.writerows(data)





oecd_path="./MEI_standardized_CCI.csv"
nber_path="./USREC.csv"
output_path="./compiled_data_OECD_standardized_CCI.csv"


# relevant_data="OECD Standardised BCI, Amplitude adjusted (Long term average=100), sa"
relevant_data="OECD Standardised CCI, Amplitude adjusted (Long term average=100), sa"
# relevant_data="Amplitude adjusted (CLI)"
# relevant_data="Normalised (CLI)"
# relevant_data="Trend restored (CLI)"
# relevant_data="12-month rate of change of the trend restored CLI"
# relevant_data="Ratio to trend (GDP)"
# relevant_data="Normalised (GDP)"
# relevant_data="Trend (GDP)"
relevant_country='United States'

start_date="1970-01"
start_date_NBER="1970-01-01" #standard date format



contents = read_from_csv(oecd_path)


#reformats the csv data
country_names=[]
country_data={}
for x in range(0, len(contents)):
	#only care about the standardized CCI data
	if contents[x][1]==relevant_data:
		country = contents[x][3]

		#adds new country to dictionary
		if country not in country_data.keys():
			country_data[str(country)]=[]
			country_names.append(country)

		country_data[str(country)].append(contents[x])




#gets monthly dates from the relevant country's data
to_save=[]
found=False
for x in range(0, len(country_data[str(relevant_country)])):

	if found:
		row = []
		row.append(str(country_data[str(relevant_country)][x][6])) #date
		row.append(country_data[str(relevant_country)][x][14]) #value
		to_save.append(row)
	else:
		if country_data[str(relevant_country)][x][6]==start_date:
			found=True




#relevant country's data has already been added, so remove its name
country_names.remove(str(relevant_country))

#adds all other country's data
for x in range(0, len(to_save)):
	date = to_save[x][0]

	print(date)
	#finds all data corresponding to date for all countries
	for y in range(0, len(country_names)):
		country_name = country_names[y]

		#iterates through country's data
		found_date=False
		for z in range(0, len(country_data[str(country_name)])):
			if country_data[str(country_name)][z][6]==date:
				to_save[x].append(country_data[str(country_name)][z][14])
				found_date=True
				break

		#if data didn't exist for date, add default of 100
		if found_date==False:
			to_save[x].append(100)



#loads NBER recession data for neural network's output
NBER = read_from_csv(nber_path)

#inserts NBER data into to_save
#NBER represents when the US is in a recession per month. 0 if not, 1 if yes.
for x in range(0, len(NBER)):

	if NBER[x][0]==start_date_NBER:
		for y in range(0, len(to_save)):


			# try:
			# 	#because we want the model to be able to predict recessions, modify the NBER so that the recessions start earlier than they actually did. 
			# 	#looks 3 months ahead
			# 	if int(NBER[x+y+1 + 3][1])==1:
			# 		to_save[y].insert(1, 1)
			# 		continue
			# except Exception as error:
			# 	# print(error)
			# 	pass

			to_save[y].insert(1, NBER[x+y+1][1])

		break





#adds header row
header=["", str(relevant_country), str(relevant_country)+" OECD"]
for x in range(0, len(country_names)):
	header.append(country_names[x])

to_save.insert(0, header)


save_to_csv(output_path, to_save)