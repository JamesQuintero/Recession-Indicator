import os
import csv

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


def save_to_csv(path, data):
		with open(path, 'w', newline='') as file:
			contents = csv.writer(file)
			contents.writerows(data)





## *) First go to http://stats.oecd.org/Index.aspx?DataSetCode=MEI_CLI ##
# *) any value over 100 for a month, indicates a recession
# *) in the left panel menu, select "Composite Leading Indicators (MEI)"
# *) click on the "Time" header label under "Country" on the graph. 
# *) Top should have "Select time range" selected. 
# *) Select the Monthly checkbox.
# *) Can use the dropdown list in the "From:" column to select the oldest date, or select the radiobox for "Select latest data", 
# and use the dropdown list corresponding to the monthly row, and select the higher number of months
# *) in the top menu, click Export, then CSV, and Download
# *) rename the file downloaded to "MEI_standardized_CCI.csv"
# *) Download CSV from https://fred.stlouisfed.org/series/USREC




# path="MEI_normalized_CLI.csv"
path="MEI_standardized_CCI.csv"

contents = read_from_csv(path)


start_date="1970-01"
# start_date_USA="1/1/1970" #because fuck excel's date handling
start_date_USA="1970-01-01" #standard date format


country_names=[]
country_data={}
for x in range(0, len(contents)):
	# print(str(x)+" | "+str(contents[x]))

	#only care about the standardized CCI data
	if contents[x][1]=="OECD Standardised CCI, Amplitude adjusted (Long term average=100), sa":
		country = contents[x][3]

		#adds new country to dictionary
		if country not in country_data.keys():
			country_data[str(country)]=[]
			country_names.append(country)

		country_data[str(country)].append(contents[x])


#gets monthly dates from the United States data
to_save=[]
found=False
for x in range(0, len(country_data['United States'])):

	if found:
		row = []
		row.append(str(country_data['United States'][x][6])) #date
		row.append(country_data['United States'][x][14]) #value
		to_save.append(row)
	else:
		# print(country_data['United States'][x][6])
		if country_data['United States'][x][6]==start_date:
			found=True




#United State's data has already been added, so remove its name
country_names.remove("United States")

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



#loads USA's NBER recession data for neural network's output
path="./USREC.csv"
NBER = read_from_csv(path)

#inserts NBER data into to_save
found_date=False
for x in range(0, len(NBER)):
	print(str(x)+" | "+str(NBER[x]))
	if NBER[x][0]==start_date_USA:
		for y in range(0, len(to_save)):
			to_save[y].insert(1, NBER[x+y+1][1])



#adds header row
header=["", "United States", "United States OECD"]
# header=["", "United States"]
for x in range(0, len(country_names)):
	header.append(country_names[x])

to_save.insert(0, header)



# save_to_csv("./compiled_data_OECD_normalized_CLI.csv", to_save)
save_to_csv("./compiled_data_OECD_standardized_CCI.csv", to_save)