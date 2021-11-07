# -*- coding: utf-8 -*-
"""

Course:         Sustainability Analysis in Python
Author:         Marron Loods
Coordinator:    Laura Scherer
Date:           November 9, 2021


Reading guide:
    
    - Code cells are numbered based on the assignment tasks
    - Tasks are listed in order except for:
        - Task 8: Radio button, which is commented out in cell 4d.1. The 
            section between #### can be commented in to enable the radio 
            button, but the cells below need to be run manually afterwards.
        - Task 9: 
            a-d Done throughout entire code
            e Code documentation automatically generated through Sphinx
        - Task 10
    - Code commented out in current file for legibility:
        - 2b.1 Tables with count of data points per year in cell 
        - 3b Sanity test to check whether the lists of countries are identical
        - 4b.1 First scatterplot
        - 4c.1 Table with outliers 

Disclaimers:
    - GUI not placed in different file
    - On my computer, the working directory file keeps changing. Therefore, I 
        made a variable current_folder. If current_folder = '' does not work,
        please copy-paste the relative path name of the folder in which the
        files are downloaded, to ensure that all files are found.
    - When you close the window in which you select the correlation coefficient,
        Python gives the error "SystemExit: 0"
    - Sometimes, the following warning is shown:
        "Figures now render in the Plots pane by default. To make them also 
        appear inline in the Console, uncheck "Mute Inline Plotting" under the 
        Plots pane options menu."
        Please follow those instructions if wanted 
        (Go to Plots, probaby in top right pane > Click on hamburger menu in top
         right corner > Uncheck Mute inline plotting)
    - To practice with writing code documentation, this has been done for three
        functions only: significance, correlation_test, and target_reached

Accompanying files:
    - functions.py
    - Data files (MS Excel): 'Goal5' (renamed after download), 
                             'Goal7' (renamed after download),
                             'TOTAL_POPULATION_BOTH_SEXES',   
                             'UNSD — Methodology
    All other files are generated while running code, but also submitted via BS                       

Steps taken from anaconda prompt:
    - New environment created and activated
    - Install: Spyder
    - Install: statsmodels, matplotlib, openpyxl, sphinx
    - Install (after previous installations!) geopandas
    
"""


#%% Libraries, packages, functions

import geopandas as gp
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import sys 
import time
from statsmodels.stats.diagnostic import lilliefors

#Prevent SettingWithCopyWarning message from appearing after "inplace = True"
pd.options.mode.chained_assignment = None


# Somehow my spyder changed the working directory all the time. 
# If it's not the same folder as file please paste the relative path + / below
# Otherwise uncomment: current_folder = ''

# current_folder = 'Documents/SAPY_local/Assignment_feedback_submission/'
current_folder = ''

sys.path.insert(1, current_folder)

# Import functions from functions.py
from functions import (significance, MD_detectOutliers, correlation_test, 
                       target_reached)


#%% Start profiling

time_dict = {}
total_time = time.time()

#%% 1.1 Import data
t = time.time()

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

goal5 = pd.read_excel(current_folder + 'Goal5.xlsx', header=[0], usecols=([5, 6, 7, 8]), sheet_name=1, skiprows=range(1771, 4351))
goal7_2 = pd.read_excel(current_folder + 'Goal7.xlsx', header=[0], usecols=([5, 6, 7, 8]), sheet_name=1)

goal5_label = 'Goal 5.5: Proportion of women in managerial positions (%)'
goal7_label ='Goal 7.2: Renewable energy share (%)'


# Profile code cell
time_dict.update({'1a': time.time() - t})

#%% 1.2 Check for missing values
t = time.time()

if (pd.notna(goal5['Value'].all()) and pd.notna(goal7_2['Value'].all())):
    print("\nGoals 5 and 7 have no missing values")
else:
    print("\nThere are missing values. Uncomment lines to determine which goals.") #WHICH LINES???
    
print("\nNote: Countries/years for which data is missing are not in the files, as the rows simply not included. Therefore, there are no values for missing data.")
print("\n----------\n")

# Profile code cell
time_dict.update({'1a': time.time() - t})

#%% 2b.1 Check number of rows per year
t = time.time()

# print("Goal 5:\n", goal5.groupby(['TimePeriod']).count())
# print("\nGoal 7:\n", goal7_2.groupby(['TimePeriod']).count())
    
year_selection_text = "2018 is the most recent year for goal 7 and both goals have sufficient data for this year. Therefore, this year is selected."
print(year_selection_text)
print("\n----------\n")

# Profile code cell
time_dict.update({'1a': time.time() - t})

#%% 2b.2 Select data for 2018
t = time.time()

year = 2018
year_string = str(year)
goal5_2018 = goal5.loc[goal5['TimePeriod'] == year]
goal7_2_2018 = goal7_2.loc[goal7_2['TimePeriod'] == year]


# DO FOR ALL CELLS, INCLUDE NAMES

# # Profile code cell
# time_dict.update({'1a': time.time() - t})

#%% 3a Sort dataframes based on country names
t = time.time()

goal5_2018.sort_values(by=['GeoAreaCode'], inplace=True)
goal7_2_2018.sort_values(by=['GeoAreaCode'], inplace=True)

#%% 3b Only keep countries that are in both lists + sanity check
t = time.time()

# Selection of dataframes made based on boolean: is the name also in the other df?
goal5_clean = goal5_2018[goal5_2018.GeoAreaCode.isin(goal7_2_2018['GeoAreaCode'])]
goal7_2_clean = goal7_2_2018[goal7_2_2018.GeoAreaCode.isin(goal5_clean['GeoAreaCode'])]

# Make a column which deducts the area codes of both datasets
# The sum of this column should be 0 if the sets are identical
goal7_2_clean['Identical'] = goal5_clean['GeoAreaCode'].to_numpy() - goal7_2_clean['GeoAreaCode'].to_numpy()
# if goal7_2_clean['Identical'].sum() == 0:
#     print("The sets of countries are identical.")
# else:
#     print("The sets of countries are not identical.")
# print("\n----------\n")

# Reset index
goal5_clean.reset_index(inplace=True)
goal7_2_clean.reset_index(inplace=True)

#%% 4a Lilliefors Test: are the samples drawn from a normal distribution?
t = time.time()

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
print(result_lillie5)          
print(result_lillie7)          

print("\n----------\n")

"""
Results: 
The p-value of goal 5.5 is 0.585
 --> Larger than 0.05 --> H0 cannot be rejected --> Potential normal distribution
The p-value of goal 7.2 is 0.009 
 --> H0 can be rejected --> Smaller than 0.05 --> No normal distribution
We can reject H0 for goal 7.2, but not for goal 5.5. 
"""
                                 

#%% 4b.1 Make scatterplot to test homoscedasticity
t = time.time()

# plt.scatter(goal5_clean['Value'], goal7_2_clean['Value'])
# plt.xlabel(goal5_label)
# plt.ylabel(goal7_label)
# plt.xlim(0, goal5_clean['Value'].max()+1)
# plt.ylim(0, goal7_2_clean['Value'].max()+1) 
# plt.legend(["country"])
# plt.savefig(current_folder+'scatter_original.png', bbox_inches='tight')
# plt.show()
# plt.close()

homoscedasticity_text = "The scatterplot shows that the data is heteroscedastic."

print(homoscedasticity_text)
print("\n----------\n")

#%% 4b.2 Inspect boxplots to observe outliers
t = time.time()

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
plt.savefig(current_folder + 'boxplots.png', bbox_inches= 'tight')
plt.show()
plt.close()

print("The boxplots show that both goals have a few outliers. For Goal 7 these are all on the high end.")
print("\n----------\n")

#%% 4c.1 Test absence of outliers with Mahalanobis distance (MD) and remove outliers
t = time.time()

# MD requires data in row instead of columns --> transpose and find outliers
data = np.transpose(np.array([goal5_clean['Value'], goal7_2_clean['Value']]))
outliers_indices = MD_detectOutliers(data, verbose=False)

print("Outliers Indices: {}\n".format(outliers_indices))
# print("Outliers:")
# for ii in outliers_indices:
#     print(data[ii])

print("After inspection, it is concluded that the ouliers are not erroneous,\n \
however, they are removed to better determine a potential relation.")                               #CHANGE?
print("\n----------\n")

# Remove outliers

goal5_incl_outliers = goal5_clean.copy()
goal7_incl_outliers = goal7_2_clean.copy()
goal5_clean.drop(outliers_indices.tolist(), inplace=True) 
goal7_2_clean.drop(outliers_indices.tolist(), inplace=True)


#%% 4c.2 Create new scatterplot without outliers
t = time.time()


plt.scatter(goal5_incl_outliers['Value'], goal7_incl_outliers['Value'], c="tab:orange")
plt.scatter(goal5_clean['Value'], goal7_2_clean['Value'], c="tab:blue")
plt.xlabel(goal5_label)
plt.ylabel(goal7_label)
plt.xlim(0, goal5_incl_outliers['Value'].max()+1)
plt.ylim(0, goal7_incl_outliers['Value'].max()+1) 
plt.legend(["outliers", "country"])
plt.savefig(current_folder+'scatter_colored_outliers.png', bbox_inches='tight')
plt.show()
plt.close()

print("After removing the outliers, the scatterplot still indicates that the data is heteroscedastic and no relation can be determined from eyeballing.")  #CHANGE?
print("\n----------\n")


#%% 4d.1 Select correlation coefficient (also contains task 8, radio button)



t = time.time()

# If radio button is commented out, default is False    
parametric_bool = [False]

print("Spearman correlation coefficient used as default, because assumptions (normality, parametric) not fulfilled.")


####### SECTION BELOW SHOULD BE COMMENTED OUT TO DISABLE RADIO BUTTON #########


# from PyQt5.QtWidgets import (QLabel, QRadioButton, QVBoxLayout, QApplication, QWidget)


# # In this variable, the selected correlation coefficient will be appended
# # Overwrites default boolean
# parametric_bool = []

# class SelectCoefficient(QWidget):

#     def __init__(self):
#         super().__init__()
#         self.init_ui()

#     def init_ui(self):
#         # Make labels and buttons
#         self.label = QLabel("Which correlation coefficient do you want to use?")
#         self.pearson = QRadioButton("Pearson's R")
#         self.spearman = QRadioButton("Spearman's R")
#         self.label2 = QLabel("")
        
#         # Connect clicking of button to function onClicked
#         self.pearson.clicked.connect(self.select)
#         self.spearman.clicked.connect(self.select)

#         # Create layout of window
#         layout = QVBoxLayout()
#         layout.addWidget(self.label)
#         layout.addWidget(self.pearson)
#         layout.addWidget(self.spearman)
#         layout.addWidget(self.label2)
        
#         # Create window
#         self.setGeometry(200, 200, 300, 150)
#         self.setLayout(layout)
#         self.setWindowTitle("Selection of correlation coefficient")

#         self.show()
        
#         # The clicked button is appended to correlation_bool
#         # and window closed after selection
#     def select(self):
#         radioBtn = self.sender()
#         if radioBtn == self.pearson:
#             parametric_bool.append(True)
#         if radioBtn == self.spearman:
#             parametric_bool.append(False)
#         if radioBtn.isChecked():
#             self.close()
    
        
# # Execute radio-button 
# if __name__ == "__main__":    
#     app = QApplication(sys.argv)
#     ex = SelectCoefficient()
#     sys.exit(app.exec_())


####### SECTION ABOVE SHOULD BE COMMENTED OUT TO DISABLE RADIO BUTTON #########


#%%  4d.2 Calculate Pearson or Spearman correlation coefficient

# Calculate correlation
correlation_result = correlation_test(parametric_bool, goal5_clean['Value'], goal7_2_clean['Value'])

# Document correlation test for output file in cell 6
correlation_name = ""

if parametric_bool[-1]:
    correlation_name += "Pearson's R"
    print("\nThe result of the " + correlation_name + " correlation test is: ", correlation_result)
if not parametric_bool[-1]:
    correlation_name +="Spearman's R"
    print("\nThe result of the  " + correlation_name + " correlation test is: ", correlation_result)
print(significance(correlation_result))

#%% 4e Print interpretation to console

interpretation_text = "\nThe results indicate that there is probably no relation \
between the percentage of population with electricity access and the \n\
proportion of women in managerial positions.\
\nIf the result had been significant, there would have been a slight trade-off between the SDGs. \
Although the indicators are very different \nand based upon many different factors, it could \
make more sense if the indicators were positively correlated, because both \
indicate some \nkind of positive development which is strived for by \
most countries. Therefore, it is expected that the measured trade-off is very insignificant."
print(interpretation_text)
print("\n----------\n")


#%% 5a.1 Read in population data and select only countries of interest
t = time.time()

# Read in data and select only countries used in analysis
population = pd.read_excel(current_folder + 'TOTAL_POPULATION_BOTH_SEXES.xlsx', header=[16], usecols=([2, 4, 75]))
population.sort_values(by=['Country code'], inplace=True)
population_clean = population[population['Country code'].isin(goal5_clean['GeoAreaCode'])]

# Make 1 dataframe with both goals and size, add population data for selected year
goals = goal5_clean.copy()
goals['Value7'] = goal7_2_clean['Value'].values
goals['Population'] = population_clean[year_string].values.astype(float)
goals.rename(columns = {'Value':'Goal5', 'Value7':'Goal7'}, inplace = True)


#%% 5a.2 Make bubble chart 
t = time.time()

# Create logical sizes from population data
goals['Sizes'] = goals['Population'] / 500

# Top 10 countries with largest population
population10 = goals.nlargest(10, 'Population') 
population10.reset_index(inplace=True)

# Make bubble chart
plt.scatter(goals['Goal5'], goals['Goal7'], s=goals['Sizes'])
for i in range(population10.shape[0]):
    plt.text(x=population10.Goal5[i]+0.5,y=population10.Goal7[i]+0.5,s=population10.GeoAreaName[i], 
          fontdict=dict(color='black',size=8))
plt.xlabel(goal5_label)
plt.ylabel(goal7_label)
plt.xlim(0, goals['Goal5'].max()+7)
plt.ylim(0, goals['Goal7'].max()+2) 
plt.savefig(current_folder + 'bubble_chart.png', bbox_inches= 'tight')
plt.show()
plt.close()


#%% 5b.1 Include population data and other info in the geodataframe of the world map
t = time.time()
        
# Download world shapefile
world = gp.read_file(gp.datasets.get_path("naturalearth_lowres"))

# Download UN file with country codes
world_match_codes = pd.read_excel(current_folder + 'UNSD — Methodology.xlsx', header=[0], usecols=([8, 9, 11]))

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

#%% 5b.2 Use function to indicate whether countries have met the target


# Add means of goals as a new column to world_all dataframe so that they can
# be accessed when applying target_reached to every row

world_all['Goal5 mean'] = world_all['Goal5'].mean()
world_all['Goal7 mean'] = world_all['Goal7'].mean()

# Determine whether the targets are reached and make new column
world_all['targets'] = world_all.apply(target_reached, axis=1)

means_text = "The means of the goals are {:.2f}% and {:.2f}%.".format(world_all['Goal5'].mean(), world_all['Goal7'].mean())
print(means_text)


#%% 5b.3 Plot world map with countries colored based on reaching of target

world_all.plot(column='targets', legend=True, figsize=(10, 5), 
               cmap='Accent', legend_kwds={'loc': 'center left'})
plt.xlabel('Latitude (°)')
plt.ylabel('Longitude (°)')
plt.xlim(-180, 180)
plt.ylim(-90, 90) 
plt.savefig(current_folder +'world_map.png', bbox_inches='tight')
plt.show()
plt.close()

world_map_text = means_text + "\n\nThe world map shows a very scattered distribution of countries in which one, \
both, or neither of the targets is met. Meeting the target here means scoring \n\
above the mean of that goal within all selected countries. No patterns can be noticed from this map."

print(world_map_text)

#%% 6 Export results to text file
t = time.time()

opening_text = "Results file for the SAPY Assignment\n" + SDGs + "\n"

lilliefors_text = "\n\n" + result_lillie5 + "\n" + result_lillie7 

correlation_text = "The results of the " + correlation_name + \
    " test are: \n\nCorrelation: " + \
        str(correlation_result[0]) + \
        "\nP-value: " + str(correlation_result[0]) + "\n" +\
            significance(correlation_result)


lines_of_text = [opening_text, year_selection_text, lilliefors_text, correlation_text, 
                 interpretation_text, world_map_text]

with open(current_folder + "Results.txt", "w") as f:
    f.write("\n".join(lines_of_text))


#%%

"""
Still to do:
    - Check printed text to console
    - Optimisation: 
        - Time sections
        - Avoid dots, local variables?  
    - Round --> string formatting?
    - Txt export
    - Betere uitleg bovenaan voor aanpassingen
    - ReadMe

Vragen laatste college:
    - GUI in ander python file
    - Na GUI file verder laten runnen
"""

