# -*- coding: utf-8 -*-
"""

Course:         Sustainability Analysis in Python
Author:         Marron Loods
Coordinator:    Laura Scherer
Date:           November 9, 2021

Research question: 
    
    Are social and environmental Sustainable Development Goals (SDGs) 
    correlated, and is there rather a trade-off or a synergy between the two?

Accompanying files:
    
    - assignment_A_functions.py
    - Data files (MS Excel): 'Goal5' (renamed after download), 
                             'Goal7' (renamed after download),
                             'TOTAL_POPULATION_BOTH_SEXES',   
                             'UNSD — Methodology
    - README.md  
    - Docs: Files for Sphinx documentation generator             
    All other files are generated while running code, but also submitted via BS                       

Steps taken from anaconda prompt:
    
    - New environment created and activated
    - Install: Spyder
    - Install: statsmodels, matplotlib, openpyxl, sphinx
    - Install (after previous installations!) geopandas
    

For the reading guide and some disclaimers, please see the README file.
"""


#%% Libraries, packages, functions

import geopandas as gp
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import sys 
from time import time
from statsmodels.stats.diagnostic import lilliefors

#Prevent SettingWithCopyWarning message from appearing after "inplace = True"
pd.options.mode.chained_assignment = None


# Use code below in case of the error: No such file or directory: 'Goal5.xlsx'
# If the working directory is not the same folder as thid current file please 
# paste the relative path + '/' below. Otherwise uncomment: current_folder = ''

# current_folder = 'Loods_Assignment/'
current_folder = ''

sys.path.insert(1, current_folder)

# Import functions from functions.py
from assignment_A_functions import (significance, MD_detectOutliers, 
                                    correlation_test, target_reached)

#%% Initiate time profiling dictionary and total time variable

time_table = {}
time_total = time()

#%% 1.1 Import data
time_cell = time() # Start timing this code cells

SDGs = """
Selected Sustainable Development Goals:
    https://unstats.un.org/sdgs/unsdg
    
    - Goal 5: Achieve gender equality and empower all women and girls
        Target 5.5: Ensure women's full and effective participation and equal 
        opportunities for leadership at all levels of decision-making in 
        political, economic and public life
        
        --> Indicator 5.5.2: Proportion of women in managerial positions (%)
    
    - Goal 7: Ensure access to affordable, reliable, sustainable and modern 
        energy for all
        Target 7.2: By 2030, increase substantially the share of renewable 
        energy in the global energy mix
        
        --> Indicator 7.2.1: Renewable energy share in the total final energy consumption (%)
"""

goal5 = pd.read_excel('Goal5.xlsx', header=[0], usecols=([5, 6, 7, 8]), sheet_name=1, skiprows=range(1771, 4351))
goal7_2 = pd.read_excel('Goal7.xlsx', header=[0], usecols=([5, 6, 7, 8]), sheet_name=1)

goal5_label = 'Goal 5.5: Proportion of women in managerial positions (%)'
goal7_label ='Goal 7.2: Renewable energy share (%)'


# Note time of running code cell in time_total dictionary
# This is repeated in each code cell
time_table['1.1'] = time() - time_cell

#%% 1.2 Check for missing values
time_cell = time()

if (pd.notna(goal5['Value'].all()) and pd.notna(goal7_2['Value'].all())):
    print("\nGoals 5 and 7 have no missing values")
else:
    print("\nThere are missing values. Uncomment lines to determine which goals.") 
    
print("\nNote: Countries/years for which data is missing are not in the files, as the rows simply not included. Therefore, there are no values for missing data.")
print("\n----------\n")


time_table['1.2'] = time() - time_cell

#%% 2b.1 Check number of rows per year
time_cell = time()

# print("Goal 5:\n", goal5.groupby(['TimePeriod']).count())
# print("\nGoal 7:\n", goal7_2.groupby(['TimePeriod']).count())
    
print("2018 is the most recent year for goal 7 and both goals have sufficient data for this year. Therefore, this year is selected.")
print("\n----------\n")

# Profile code cell
time_table['2b.1'] = time() - time_cell

#%% 2b.2 Select data for 2018
time_cell = time()

year = 2018
year_string = str(year)
goal5_2018 = goal5.loc[goal5['TimePeriod'] == year]
goal7_2_2018 = goal7_2.loc[goal7_2['TimePeriod'] == year]


time_table['2b.2'] = time() - time_cell

#%% 3a Sort dataframes based on country names
time_cell = time()

goal5_2018.sort_values(by=['GeoAreaCode'], inplace=True)
goal7_2_2018.sort_values(by=['GeoAreaCode'], inplace=True)

time_table['3a'] = time() - time_cell

#%% 3b Only keep countries that are in both lists + sanity check
time_cell = time()

# Selection of dataframes made based on boolean: is the name also in the other df?
goal5_clean = goal5_2018[goal5_2018.GeoAreaCode.isin(goal7_2_2018['GeoAreaCode'])]
goal7_2_clean = goal7_2_2018[goal7_2_2018.GeoAreaCode.isin(goal5_clean['GeoAreaCode'])]

# Make a column which deducts the area codes of both datasets
# The sum of this column should be 0 if the sets are identical
goal7_2_clean['Identical'] = goal5_clean['GeoAreaCode'].to_numpy() - goal7_2_clean['GeoAreaCode'].to_numpy()
if goal7_2_clean['Identical'].sum() == 0:
    print("The sets of countries are identical.")
else:
    print("The sets of countries are not identical.")
print("\n----------\n")

# Reset index
goal5_clean.reset_index(inplace=True)
goal7_2_clean.reset_index(inplace=True)

time_table['3b'] = time() - time_cell

#%% 4a Lilliefors Test: are the samples drawn from a normal distribution?
time_cell = time()

"""
Lilliefors test
H0 : Data come from a normal distribution
H1 : Data don't come from  normal distribution
If p < 0.05, we can reject the null-hypothesis     
"""

# Lilliefors test to determine whether samples are normally distributed
lillie5 = lilliefors(goal5_clean['Value'], dist='norm')
lillie7 = lilliefors(goal7_2_clean['Value'], dist='norm')

# Print results and whether the results are significant
result_lillie5 = "Lilliefors results Goal 5: " + str(lillie5)  + "\n" + significance(lillie5)
result_lillie7 = "\nLilliefors results Goal 7: " + str(lillie7) + "\n" + significance(lillie7)

print(result_lillie5 + "\n" + result_lillie7) 
print("\n----------\n")

"""
Results: 
The p-value of goal 5.5 is 0.585
 --> Larger than 0.05 --> H0 cannot be rejected --> Potential normal distribution
The p-value of goal 7.2 is 0.009 
 --> H0 can be rejected --> Smaller than 0.05 --> No normal distribution
We can reject H0 for goal 7.2, but not for goal 5.5. 
"""
                           
time_table['4a'] = time() - time_cell      

#%% 4b.1 Make scatterplot to test homoscedasticity
time_cell = time()

plt.scatter(goal5_clean['Value'], goal7_2_clean['Value'])
plt.xlabel(goal5_label)
plt.ylabel(goal7_label)
plt.xlim(0, goal5_clean['Value'].max()+1)
plt.ylim(0, goal7_2_clean['Value'].max()+1) 
plt.legend(["country"])
# plt.savefig('scatter_original.png', bbox_inches='tight')
plt.close()

homoscedasticity_text = "The scatterplot shows that the data is heteroscedastic."

time_table['4b.1'] = time() - time_cell

#%% 4b.2 Inspect boxplots to observe outliers
time_cell = time()

plt.figure(1)
plt.subplot(121)
plt.boxplot(goal5_clean['Value'])
plt.ylabel('Percentage (%)')
plt.xticks([]) # Remove 1 from x axis 
plt.xlabel('Goal 5')
plt.ylim(goal5_clean['Value'].min()-1, goal5_clean['Value'].max()+1) 
plt.subplot(122)
plt.boxplot(goal7_2_clean['Value'])
plt.xticks([]) 
plt.xlabel('Goal 7')
plt.ylim(goal7_2_clean['Value'].min()-1, goal7_2_clean['Value'].max()+1)
# plt.savefig('box.png', bbox_inches= 'tight')
plt.close()


time_table['4b.2'] = time() - time_cell

#%% 4c.1 Test absence of outliers with Mahalanobis distance (MD) and remove outliers
time_cell = time()

# MD requires data in row instead of columns --> transpose and find outliers
data = np.transpose(np.array([goal5_clean['Value'], goal7_2_clean['Value']]))
outliers_indices = MD_detectOutliers(data, verbose=False)

print("Outliers Indices: {}\n".format(outliers_indices))
# print("Outliers:")
# for ii in outliers_indices:
#     print(data[ii])

print("After inspection of boxplots, it is concluded that the ouliers are not erroneous,\n \
however, they are removed to better determine a potential relation.")
print("\n----------\n")

# Create copy with outliers and make new dataframes without outliers
goal5_incl_outliers = goal5_clean.copy()
goal7_incl_outliers = goal7_2_clean.copy()
goal5_clean.drop(outliers_indices.tolist(), inplace=True) 
goal7_2_clean.drop(outliers_indices.tolist(), inplace=True)

time_table['4c.1'] = time() - time_cell

#%% 4c.2 Create new scatterplot with colored outliers
time_cell = time()

plt.scatter(goal5_incl_outliers['Value'], goal7_incl_outliers['Value'], c="tab:orange")
plt.scatter(goal5_clean['Value'], goal7_2_clean['Value'], c="tab:blue")
plt.xlabel(goal5_label)
plt.ylabel(goal7_label)
plt.xlim(0, goal5_incl_outliers['Value'].max()+1)
plt.ylim(0, goal7_incl_outliers['Value'].max()+1) 
plt.legend(["Outlier", "Country"])
# plt.savefig('scatter_colored_outliers.png', bbox_inches='tight')
plt.close()

print("After removing the outliers, the scatterplot still indicates that the data is heteroscedastic and no relation can be determined from eyeballing.")  #CHANGE?
print("\n----------\n")

time_table['4c.2'] = time() - time_cell

#%% 4d.1 Select correlation coefficient (also contains task 8, radio button)
time_cell = time()

# If radio button is commented out, default is False    
parametric_bool = False

parametric_text = "Spearman correlation coefficient set up as default, because assumptions (normality, parametric) not fulfilled.\n"

####### SECTION BELOW SHOULD BE COMMENTED OUT TO DISABLE RADIO BUTTON #########

# parametric_text = "Radio button enabled.\n"

# # Imports  
# from PyQt5.QtWidgets import  QApplication
# from assignment_A_functions import SelectCoefficient

# app = QApplication(sys.argv)
# ex = SelectCoefficient()
# ex.show() 
# app.exec_()
# parametric_bool = ex.parametric_bool

####### SECTION ABOVE SHOULD BE COMMENTED OUT TO DISABLE RADIO BUTTON #########

time_table['4d.1 (no radio button)'] = time() - time_cell

#%%  4d.2 Calculate Pearson or Spearman correlation coefficient
time_cell = time()

# Calculate correlation
correlation_result = correlation_test(parametric_bool, goal5_clean['Value'], goal7_2_clean['Value'])

# Document correlation test for output file in cell 6
correlation_name = ""
correlation_type = ""

if parametric_bool:
    correlation_name += "Pearson's R"
    correlation_type += "parametric"
if not parametric_bool:
    correlation_name +="Spearman's R"
    correlation_type += "non-parametric"

print(parametric_text)
print("Correlation test used:", correlation_name)
print("This test is " + correlation_type + ".")
time_table['4d.2'] = time() - time_cell

#%% 4e Write interpretation text
time_cell = time()

interpretation_text = "\nThe results indicate that there is probably no relation \
between the percentage of population with electricity access and the \n\
proportion of women in managerial positions.\
\n\nIf the result had been significant, there would have been a slight trade-off between the SDGs. \
Although the indicators are very different \nand based upon many different factors, it could \
make more sense if the indicators were positively correlated, because both \
indicate some \nkind of positive development which is strived for by \
most countries. Therefore, it seems logical that the measured trade-off is very insignificant."

time_table['4e'] = time() - time_cell

#%% 5a.1 Read in population data and select only countries of interest
time_cell = time()

# Read in data and select only countries used in analysis
population = pd.read_excel('TOTAL_POPULATION_BOTH_SEXES.xlsx', header=[16], usecols=([2, 4, 75]))
population.sort_values(by=['Country code'], inplace=True)
population_clean = population[population['Country code'].isin(goal5_clean['GeoAreaCode'])]

# Make 1 dataframe with both goals, add population data for selected year
goals = goal5_clean.copy()
goals['Value7'] = goal7_2_clean['Value'].values
goals['Population'] = population_clean[year_string].values.astype(float)

# Change column names
goals.rename(columns = {'Value':'Goal5', 'Value7':'Goal7'}, inplace = True)

time_table['5a.1'] = time() - time_cell

#%% 5a.2 Make bubble chart 
time_cell = time()

# Create logical sizes from population data
goals['Sizes'] = goals['Population'] / 500

# Top 10 countries with largest population
population10 = goals.nlargest(10, 'Population') 

# Drop USA because of overlapping labels. Index value is the same as in goals.
US_index = population10.loc[population10['GeoAreaName'] == 'United States of America'].index.values[0]
population10.drop([US_index], inplace=True) 
population10.reset_index(inplace=True) # Reset index for the for-loop

# Make bubble chart
plt.scatter(goals['Goal5'], goals['Goal7'], s=goals['Sizes'])
for i in range(population10.shape[0]):
    plt.text(x=population10.Goal5[i]+0.5,y=population10.Goal7[i]+0.5,s=population10.GeoAreaName[i], 
          fontdict=dict(color='black',size=8))
plt.text(x=goals.Goal5[US_index]+0.5,y=goals.Goal7[US_index]+2,s=goals.GeoAreaName[90], 
      fontdict=dict(color='black',size=8))
plt.xlabel(goal5_label)
plt.ylabel(goal7_label)
plt.xlim(0, goals['Goal5'].max()+7)
plt.ylim(0, goals['Goal7'].max()+2) 
plt.savefig('bubble.png', bbox_inches= 'tight')
plt.close()

time_table['5a.2'] = time() - time_cell

#%% 5b.1 Include population data and other info in the geodataframe of the world map
time_cell = time()
      
# Download world shapefile
world = gp.read_file(gp.datasets.get_path("naturalearth_lowres"))

# Download UN file with country codes
world_match_codes = pd.read_excel('UNSD — Methodology.xlsx', header=[0], usecols=([8, 9, 11]))

# Select countries in the UN file that are also in goals
goals_match_code = world_match_codes[world_match_codes['Country or Area'].isin(goals['GeoAreaName'])]

# Sort values in goals_match_codes and add codes to goals
goals_match_code.sort_values(by=['M49 Code'], inplace=True)
goals['iso_a3'] = goals_match_code['ISO-alpha3 Code'].values

# Some countries are missing in the world map, probably because they are too small
# However, the country codes of CYP, FRA and NOR had incorrect values
# These are changed below.
world.loc[world['name'] == 'France', 'iso_a3'] = 'FRA'
world.loc[world['name'] == 'Norway', 'iso_a3'] = 'NOR'
world.loc[world['name'] == 'Cyprus', 'iso_a3'] = 'CYP'

# Select the countries of the world that were selected in this assignment
world_selection = world[world['iso_a3'].isin(goals['iso_a3'])]

# Make smaller selection of goals which only containts countries in
# world_selection, sort values, drop unnecessary collumns and merge
# with world_selection
goals_selection_world = goals[goals['iso_a3'].isin(world_selection['iso_a3'])]
goals_selection_world.sort_values(by=['iso_a3'], inplace=True)
goals_selection_world.drop(['index', 'GeoAreaName', 'Population', 'TimePeriod', 'Sizes'], axis=1, inplace=True)
world_all = world.merge(goals_selection_world, on='iso_a3', how='left')
world_all.reset_index(inplace=True)

time_table['5b.1'] = time() - time_cell

#%% 5b.2 Use function to indicate whether countries have met the target
time_cell = time()

# Add means of goals as a new column to world_all dataframe so that they can
# be accessed when applying target_reached to every row

world_all['Goal5 mean'] = world_all['Goal5'].mean()
world_all['Goal7 mean'] = world_all['Goal7'].mean()

# Determine whether the targets are reached and make new column
world_all['targets'] = world_all.apply(target_reached, axis=1)

means_text = "\nThe means of the goals are {:.2f}% and {:.2f}%.".format(world_all['Goal5'].mean(), world_all['Goal7'].mean())

print("\n----------\n")

time_table['5b.2'] = time() - time_cell

#%% 5b.3 Plot world map with countries colored based on reaching of target
time_cell = time()

world_all.plot(column='targets', legend=True, figsize=(10, 5), 
               cmap='Accent', legend_kwds={'loc': 'center left'})
plt.xlabel('Latitude (°)')
plt.ylabel('Longitude (°)')
plt.xlim(-180, 180)
plt.ylim(-90, 90) 
plt.savefig('map.png', bbox_inches='tight')
plt.close()

world_map_text = "The world map shows a very scattered distribution of countries in which one, \
both, or neither of the targets is met. Meeting the target here means scoring \n\
above the mean of that goal within all selected countries. No patterns can be noticed from this map either, which is in line with previous results."
print(world_map_text)
print("\n----------\n")

time_table['5b.3'] = time() - time_cell

#%% 6 Export results to text file
time_cell = time()

opening_text = "Results file for the SAPY Assignment\n" + SDGs + "\n"

year_selection_text = "Selected year: " + year_string


correlation_text = "\n\nThe " + correlation_name + " test is performed. This test is " \
    + correlation_type + ".\nThe results of the test are: \n\nCorrelation: " + \
        str(round(correlation_result[0], 4)) + \
        "\nP-value: " + str(round(correlation_result[1], 4)) + "\n" +\
            significance(correlation_result)


lines_of_text = [opening_text, year_selection_text, 
                 correlation_text, interpretation_text]

with open('sdg_correlation.txt', "w") as f:
    f.write("\n".join(lines_of_text))

time_table['6'] = time() - time_cell

#%% 7 Update total time in dictionary

time_table['total'] = time() - time_total

"""
Documenting the time gives the following code cells as taking the most time:
    (listed from taking the most to the least time)
    - Total time
    - 1.1 Import data 
    - 5b.3 Plot world map 
    - 5a.1 Import population data and select only countries of interest
    - 4c.2 Create new scatterplot 
    - 4b.2 Create boxplots
    - 5a.2 Create bubble chart
    - 5b.1 Import country code file and make geodataframe
    - 4d.1 Run radio button


Although the exact time differs per run, partially depending on other 
background processes, the order remains more or less the same. The cells above 
are the ones that take more than 0.01 second to run. It is visible that this 
regards plots and data imports. Considering this consists of importing or 
creating files/a window outside of Spyder, it makes sense that this take 
slightly more time. 

Other than that, the code cells are written fairly concisely, so further
optimisation is not considered necessary.
    
"""

#%% 10 Github

"""
Please find the github for this assignment on the following website:
    https://github.com/marronlds/Loods_SAPY_2021

The GitHub is used for practicing and does not contain the final code
for the assignment.
"""
#%%