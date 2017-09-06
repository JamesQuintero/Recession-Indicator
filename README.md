# Recession-Indicator
Uses Machine Learning to detect whether the United States is entering a recession by training a neural network with OECD's (Organisation For Economic Co-Operation and Development) CLI indicator. "The OECD CLI is designed to provide qualitative information on short-term economic movements".


### Python libraries needed can be installed using Anaconda on Windows. 
* numpy
* pandas
* keras (needs tensorflow and theano, with tensorflow being the backend to keras)


### Steps for obtaining country data: 
1. First go to http://stats.oecd.org/Index.aspx?DataSetCode=MEI_CLI   
    Any value over 100 for a month, indicates an economic downturn. The higher the number, the better.
2. In the left panel menu, select "Composite Leading Indicators (MEI)"
3. Click on the "Time" header label under "Country" on the graph.   
    Top should have "Select time range" selected. 
4. Select the Monthly checkbox.
5. Can use the dropdown list in the "From:" column to select the oldest date, or select the radiobox for "Select latest data", and use the dropdown list corresponding to the monthly row, and select the higher number of months
6. In the top menu, click Export, then CSV, and Download
7. Rename the file downloaded to "MEI_standardized_CCI.csv"
8. Download CSV from https://fred.stlouisfed.org/series/USREC


### Steps for running: 
1. Run compile_data.py once country data is properly renamed and placed in the folder. 
2. Run ANN_recession.py   
    Percentage for current recession will be given, and percentages for all previous months will be output to US_recession_percentages.csv
