import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib.patches as mpatches
from datetime import datetime
import sys

def map_and_graph():
	covid_data_in_us = pd.read_csv("time_series_covid19_deaths_US.csv")

	covid_data_in_us = covid_data_in_us.rename(columns={"Admin2":"County", "Province_State":"State"})

	california = covid_data_in_us["State"] == "California"
	covid_data_in_us = covid_data_in_us[california]

	unused_columns = ["UID", "iso2", "iso3", "code3", "FIPS", "Country_Region", "Combined_Key", "State"]
	covid_data_in_us = covid_data_in_us.drop(columns = unused_columns)

	covid_data_in_us = covid_data_in_us.set_index("County")

	deaths_each_day = covid_data_in_us
	deaths_each_day = deaths_each_day.drop(columns = ["Lat", "Long_"])

	deaths = list(covid_data_in_us[covid_data_in_us.columns[-1]])  #"11/3/20"
	lat = list(covid_data_in_us["Lat"])
	long = list(covid_data_in_us["Long_"])

	modified_deaths = []
	for i in deaths:
	    modified_deaths.append(i / 50)

	california = mpimg.imread("california.png")
	fig, (ax0, ax1) = plt.subplots(nrows = 1, ncols = 2, figsize=(15,10))
	ax0.scatter(long, lat, alpha = 0.4, s = modified_deaths, color="red")
	ax0.imshow(california, extent=[-124.55, -113.00, 32.45, 42.05])
	ax0.set_title("COVID-19 Deaths in California by County", fontsize = 15, pad = 10)

	covid_data_in_us = pd.read_csv("time_series_covid19_deaths_US.csv")
	deaths_in_california = pd.read_csv("time_series_covid19_deaths_US.csv")

	#Plotting the graph
	#cleaning up deaths_in_california data frame
	deaths_in_california = deaths_in_california.rename(columns={"Admin2":"County", "Province_State":"State"})
	deaths_in_california = deaths_in_california[deaths_in_california["State"] == "California"]

	total_deaths_in_california = deaths_in_california[deaths_in_california.columns[-1]].sum()

	unused_columns = ["UID", "iso2", "iso3", "code3", "FIPS", "Long_", "Lat", "Country_Region", "Combined_Key", "State"]
	deaths_in_california = deaths_in_california.drop(columns=unused_columns)
	deaths_in_california = deaths_in_california.set_index("County")

	last_col = deaths_in_california.shape[1]-1
	for col in range(last_col, 0, -1):
		deaths_in_california.iloc[:,col] = deaths_in_california.iloc[:,col] - deaths_in_california.iloc[:,col-1]

	#cleaning up covid_data_in_us data frame
	covid_data_in_us = covid_data_in_us.rename(columns={"Admin2":"County", "Province_State":"State"})

	california = covid_data_in_us["State"] == "California"
	covid_data_in_us = covid_data_in_us[california]


	unused_columns = ["UID", "Lat", "Long_", "iso2", "iso3", "code3", "FIPS", "Country_Region", "Combined_Key", "State"]
	covid_data_in_us = covid_data_in_us.drop(columns = unused_columns)

	print("Please type in the County you want to see the data for")
	county = input()
	users_input = covid_data_in_us["County"] == county
	covid_data_in_us = covid_data_in_us[users_input]

	covid_data_in_us = covid_data_in_us.set_index("County")

	first_column = covid_data_in_us.columns.get_loc("1/22/20")
	last_column = covid_data_in_us.shape[1] - 1

	for col in range(last_column, 0, -1):
		covid_data_in_us.iloc[:,col] = covid_data_in_us.iloc[:,col] - covid_data_in_us.iloc[:,col-1]
	
	#values for daily deaths in a selected county
	y_values = covid_data_in_us.loc[county][first_column:last_column]
	x_values = covid_data_in_us.loc[county][first_column:last_column].index

	#values for daily deaths in the California
	y_values_all = []
	for i in x_values:
		y_values_all.append(deaths_in_california[i].sum())

    #converting dates into a suitable format for graphing with matplotlib
	x_values = [datetime.strptime(day, '%m/%d/%y') for day in x_values]

	#making lists for seven day average data
	n = 0
	z = 7
	seven_day_average_deaths_county = []
	seven_day_average_deaths_california = []
	seven_day_average_days = []

	while z <= last_column:
		summation_county = 0
		summatoin_california = 0
		for i in range(n, z):
			summation_county += y_values[i]
			summatoin_california += y_values_all[i]
		n = n + 1
		z = z + 1
		seven_day_average_deaths_county.append((summation_county / 7).round(1))
		seven_day_average_deaths_california.append((summatoin_california / 7).round(1))

	for i in range(6, last_column):
		seven_day_average_days.append(x_values[i])

	#total deaths in selected county
	total_county_deaths = sum(y_values)

	#creating a legend with total deaths in California and selected county
	black_patch = mpatches.Patch(color="black", label="California Total = {}".format(total_deaths_in_california))
	green_patch = mpatches.Patch(color="green", label="{} Total = {}".format(county, total_county_deaths))

	#plotting the graph
	ax1.yaxis.grid(True)
	ax1.plot(seven_day_average_days, seven_day_average_deaths_california, color="black")
	ax1.fill_between(seven_day_average_days, seven_day_average_deaths_california, color="black", alpha = 0.9)
	ax1.bar(x_values, y_values, width=1, color="green", alpha=0.7)
	ax1.legend(handles=[black_patch, green_patch], fontsize=15)
	ax1.plot(seven_day_average_days, seven_day_average_deaths_county, "-", color="yellow")
	ax1.set_title("Daily Covid-19 Deaths in {} County".format(county), fontsize=15, pad=10)
	ax1.set_ylabel('Deaths per Population Desnity', labelpad=2, fontsize=15)
	ax1.set_xlabel('Day', labelpad=2, fontsize=15)
	plt.tight_layout()
	plt.show()

map_and_graph()










