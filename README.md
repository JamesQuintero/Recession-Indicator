# Recession-Indicator
Uses Machine Learning to detect whether the United States is entering a recession by training a neural network with OECD's (Organisation For Economic Co-Operation and Development) CLI indicator. "The OECD CLI is designed to provide qualitative information on short-term economic movements".

### ` As of 09-2019, the United States has a 0.01% chance of heading into a recession within the next month.`This is an increase from 0.00% in 08-2019. 

---

The model looks at each month and gives a percentage represent the likelihood of the United States entering a recession for the next month. It's typically 0.00%, but it'll sometimes be 0.1% or 0.2%. Once it gets above 1.0%, it's time to take notice. 

The model tends to start rising from 0.0% when a recession is coming. 

| Visualizing The Model |
| :-------------: |
| The recession indicator model tends to start rising from 0 when a recession is coming, and equal 1 when a recession is in full swing. ![Preview](https://i.imgur.com/tY3HhZJ.jpg)      |
| A recession is occurring when the NBER value is 1. ![Preview](https://i.imgur.com/JecIIou.jpg)      | 
| Overlapping the indicator model graph and the actual recession graph. ![Preview](https://i.imgur.com/IAoGDmO.jpg) |


Overfitting possibility? Most definitely. But when the model was trained on recession data before the Great Recession, it was still able to predict the recession and subsequent market pull-backs in 2011 and 2015. 

---




### Python libraries needed can be installed using Anaconda on Windows. 
* numpy
* pandas
* keras (needs tensorflow and theano, with tensorflow being the backend to keras)


### Steps for obtaining country data: 
1. First go to http://stats.oecd.org/Index.aspx?DataSetCode=MEI_CLI
2. In the left panel menu, select "Composite Leading Indicators (MEI)"
3. Select "OECD Standardised CCI, Amplitude adjusted (Long term average=100), sa" for the dropdown next to Subject  
    Any value below 100 for a month, indicates economic growth below that country's average. The higher the number past 100, the better.
4. Click on the "Time" header label under "Country" on the graph.   
    Top should have "Select time range" selected. 
5. Select the Monthly checkbox.
6. Can use the dropdown list in the "From:" column to select the oldest date, or select the radiobox for "Select latest data", and use the dropdown list corresponding to the monthly row, and select the higher number of months.
	Should pick starting from 1970, or 520- months. Data before 1970 is inaccurate or not available. 
7. In the top menu, click Export, then CSV, and Download.
8. Rename the file downloaded to "MEI_standardized_CCI.csv", and move to the root project folder.
9. Download CSV from https://fred.stlouisfed.org/series/USREC


### Steps for running: 
1. Run compile_data.py once country data is properly renamed and placed in the folder. 
2. Run ANN_recession.py   
    * Percentage for current recession will be given, and percentages for all previous months will be output to US_recession_percentages.csv  
    * If you want to train the model yourself, delete "recession_indicator_model.h5", and run ANN_recession.py again. 
