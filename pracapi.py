# Import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from ApiAccessor import ApiAc
from DataManipulation import DataM
from OutputData import OutData

# Determine what NFL players are getting arrested for (referred to as 'Categories' in code)
input_data = ApiAc("http://nflarrest.com/api/v1/crime")
nfl_data = input_data.getApi()

# Create dataframe to iterate through to get more data
input_nfl = DataM(nfl_data)
input_nfl_data = input_nfl.createFrame(nfl_data,['Category'])

# Create usable, functional dataframes needed for analysis (time and team)
time_data = pd.DataFrame()
team_data = pd.DataFrame()
time_data_count = pd.DataFrame()

# Iterate through each category and pull info about each category from API to use in analysis
for i, row in input_nfl_data.iterrows():
	nfl_category = row['Category']
	
	# The following code creates a dataframe with time data (Month, Year).
        # Number of Arrests/ month year and Category is also included
	data_time = ApiAc("http://nflarrest.com/api/v1/crime/timeline/%s" %nfl_category)
	data_time1 = data_time.getApi()
	data_time2 = DataM(data_time1)
	data_time2 = data_time2.createFrame(data_time1, ['arrest_count','Year', 'Month'])
	data_time2['Category'] = pd.Series(nfl_category, index = data_time2.index)
	# You can save the time_data dataframe in Excel or CSV if you want
	time_data = pd.concat([time_data, data_time2])
	
	# The following 2 lines of code makes subsetting the data easier	
	arrest_c = DataM(data_time2)
	arrest_c_array = arrest_c.makeIntegerArray(data_time2, 'arrest_count') 
	
	# Set count_time to 0 so that we can count the number of crimes per category
	count_time = 0
	
	for l in arrest_c_array:
		count_time  = count_time + l
	
	# Create a dataframe with the number of crimes committed by category
	time_data_c = pd.DataFrame({'count': [count_time]})
	time_data_c['Category'] = pd.Series(nfl_category, index = data_time2.index)
	
	time_data_count = pd.concat([time_data_count, time_data_c])

# The following makes individual arrays for each variable to output data
	# The following arrays will be used later as needed
time_data_var = DataM(time_data)

month_array = time_data_var.makeIntegerArray(time_data, 'Month')
year_array = time_data_var.makeIntegerArray(time_data, 'Year')
arrest_count_array =  time_data_var.makeIntegerArray(time_data, 'arrest_count')

# Same concept - this time category specific (from the count_time variable above)
	# This array will be used first for exploratory analysis
arrest_count_var = DataM(time_data_count)
arrest_count_array2 = arrest_count_var.makeIntegerArray(time_data_count, 'count')

# Make one array for the category variable - this one does not need to be an integer
category_array = np.array(time_data_count['Category'])

# First bar graph attempt code below. Creates bar graph for every category
	# LEARNED: There are a lot of categories with little information. 
	# I kept this code so that you can see my thought process. 
	# I would not normally re-print the graph every time	
graph1 = OutData(category_array)
graph1.barGraph(category_array, arrest_count_array2)

# Set 'Category' to Other if count < 8 (to better understand data)
time_data_count['Category_bin'] = 'Other'
time_data_count['Category_bin'][time_data_count['count'] > 8] = time_data_count['Category']

# For iteration through 'Other_variable' to get count
other_count = 0
# Iterate through each category bin and count others
for x, row in time_data_count.iterrows():
	count = row['count']

	if count < 8:
		other_count = other_count + count
		

# Create arrays and modify other variables for the graph
# Creates 'other' category_bin using count above, replaces new variable with all category_bin = other
other_count_frame = pd.DataFrame({'count': [other_count], 'Category': ['Other'], 'Category_bin': ['Other']})
time_data_count = time_data_count[time_data_count.Category_bin != 'Other']
time_data_count = pd.concat([time_data_count, other_count_frame])

# Creates arrays for graph
category_bin_array = np.array(time_data_count['Category_bin'])

arrest_count_var2 = DataM(time_data_count)
arrest_count_array_bin = arrest_count_var2.makeIntegerArray(time_data_count, 'count')

# Graph the data
# This graph looks much better. Ideally would know more about crime and would have better
	# grouped the other variables because category is quite large
graph2 = OutData(category_bin_array)
graph2.barGraph(category_bin_array, arrest_count_array_bin)

# Creates percent of total for more information about data when printed
#total = arrest_count_array_bin.sum()
#time_data_count['percent'] = (time_data_count['count'] / total) * 100
percent = DataM(time_data_count)
time_data_count = percent.createPercent(arrest_count_array_bin, time_data_count, 'count')

# Print data for another view
print (time_data_count)

# The next code groups and analyzes the crime data by year.

# Create year array to iterate through and group variables
	
	# Also want to look at DUI specifically because 25% NFLers are getting arrested for this crime.
		# Biggest crime by far.
Dui_time_data = time_data[time_data.Category == 'DUI']

# Create list to loop through so that you only have to write this code once
dataset_loop_list = [time_data, Dui_time_data]

for k in dataset_loop_list:
	year_group = ['2000', '2001', '2002', '2003', '2004', '2005', '2006', '2007', '2008', '2009','2010', '2011', '2012', '2013', '2014', '2015', '2016','2017']
	dic1 = {}

	for z in year_group:
		# Count crime data overall by year
		pre_sum_var = DataM(k[k.Year == z])
		sum_var = pre_sum_var.makeIntegerArray(k[k.Year == z], 'arrest_count')
		dic1["{0}".format(z)] = sum_var.sum()

	# Dictionary as created is difficult to change into a pandas dataframe. 
		# Opted to create a list out of the dictionary and convert
	year_count_list = []
	for key, value in dic1.iteritems():
		temp = [int(key),value]
		year_count_list.append(temp)

	# Convert list to DataFrame and sort by year
	year_count = DataM(year_count_list)
	arrest_by_year = year_count.createFrame2(year_count_list,['Year', 'Number of Arrests'])
	sorted_year_count = arrest_by_year.sort_values(by='Year')

	# Create arrays from correctly ordered data
	year_count_array = np.array(sorted_year_count['Year'])
	crime_count_array = np.array(sorted_year_count['Number of Arrests'])

	# Graph data
	crime_by_year_graph = OutData(year_count_array)
	crime_by_year_graph.barGraph(year_count_array, crime_count_array)

	# Print data with percents for another view of data
	percent = DataM(sorted_year_count)
	arrest_by_year = percent.createPercent(crime_count_array, sorted_year_count, 'Number of Arrests')

	print (arrest_by_year)
				
# DUI arrests do not vary much from other arrests (subjective note)