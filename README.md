# Assignment Sustainable Analysis in Python
This folder contains the code for a correlation analysis of two Sustainable Development Goals (SDGs).

Research question:  Are social and environmental Sustainable Development Goals (SDGs) correlated, and is there 
rather a trade-off or a synergy between the two?

Selected Sustainable Development Goals:
- **Goal 5:** Achieve gender equality and empower all women and girls
  - **Target 5.5:** Ensure women's full and effective participation and equal opportunities for leadership 
    at all levels of decision-making in political, economic and public life
    - **Indicator 5.5.2:** Proportion of women in managerial positions (%)
- **Goal 7:** Ensure access to affordable, reliable, sustainable and modern energy for all
  - **Target 7.2:** By 2030, increase substantially the share of renewable energy in the global energy mix
    - **Indicator 7.2.1:** Renewable energy share in the total final energy consumption (%)

## Contents
### Code files
- **assignment_A_functions.py:** Functions used in the main code
- **assignment_A_main.py:** Main python code 

### Data files
- **Goal5.xlsx:** Sustainable Development Goal 5 data - Gender Equality
- **Goal7.xlsx:** Sustainable Development Goal 7 data - Affordable and Clean Energy
- **TOTAL_POPULATION_BOTH_SEXES.xlsx:** Population data of all countries
- **UNSD — Methodology.xlsx:** File with all countries and different country codes

### Files that are also generated by the code
- **sdg_correlation.txt:** Results of the analysis
- **box.png:** Two boxplots of the SDGs
- **bubble.png:** Bubble chart of all selected countries, their score for both goals, and sizes based on population data
- **map.png:** A world map which indicates whether countries have met one, two, or both of the SDG targets 
(i.e. score above the mean of all selected countries
- **scatter_colored_outliers.png:** Scatterplot of all selected countries with marked outliers 
(detected with Mahalanobis Distance) 
- **scatter_original.png:** Scatterplot of all selected countries

### Assignment description
- **SAPY_assignment.pdf:** Description of assignment, provided by Leiden University

### Folders
- **Sphinx:** Files for (automatic) documentation generation
  The documentation pages can be found in Sphinx > _build > html > functions.html
- **pycache:** Related to Sphinx

## Installation
- **Required steps from prompt:**
  1. New environment created and activated
  2. Install: Spyder
  3. Install: statsmodels, matplotlib, openpyxl
  4. Install (after previous installations!) geopandas
  5. Install sphinx
  
- **Imports:** geopandas, pandas, matplotlib.pyplot, numpy, sys, time, statsmodels.stats.diagnostic

### Usage
The code can be run in its entirety. In code cell 4d.1, the radio button is commented out. This button selects 
the correlation coefficient used in the next cell. Uncomment the code between ##### in cell 4d.1 to use the 
radio button. After this, the rest of the code in the file needs to be run manually. Spearson's R correlation
coefficient is used as default, based on the findings in the analysis.

### Reading guide:
    
- For the full description of this assignment see SAPY_assignment.pdf in the folder of this code.
- Code cells are numbered based on the assignment tasks.
- Tasks are listed in order except for:
  - Task 8: Radio button (see explanation under "Running"
  - Task 9: 
    - a-d Done throughout entire code.
    - e Code documentation automatically generated through Sphinx.
  - Task 10
- Code commented out in current file to avoid spamming console/files:
  - 2b.1 Tables with count of data points per year in cell 
  - 3b Sanity test to check whether the lists of countries are identical
  - 4b.1 First scatterplot savefig
  - 4b.2 Boxplot savefig
  - 4c.1 Table with outliers 
  - 4c.2 New scatterplot with outliers in color savefig

### Disclaimers:
- GUI not placed in different file                                             
- On my computer, the GUI comes to the front, but I don't know for sure if this also happens on other computers.
- On my computer, the working directory file keeps changing. Therefore, I made a variable current_folder. 
  If current_folder = '' does not work, please copy-paste the relative path name of the folder in which the 
  current file is stored, to ensure that all files are found.
- When you close the window in which you select the correlation coefficient, Python gives the error "SystemExit: 0"
- After selecting with the GUI, the rest of the code needs to be rerun
- Sometimes, the following warning is shown:
  "Figures now render in the Plots pane by default. To make them also appear inline in the Console, uncheck 
  "Mute Inline Plotting" under the Plots pane options menu." Please follow those instructions if wanted 
 (Go to Plots, probaby in top right pane > Click on hamburger menu in top right corner > Uncheck Mute inline plotting)
- To practice with writing code documentation, this has been done for three
  functions only: significance, correlation_test, and target_reached (not for Mahalanobis Distance or the GUI)
- Statistical test results are not rounded in the console or Results.txt
- The documentation was generated when the python files were still called differently namely "assignment" and "functions".
  Therefore the pages in the readthedocs are still called this way. Please see the functions.html file for the documentation.
- The GitHub is only updated a few times to practice with git, but is not completely up to date. Please see the uploaded
  files in the zipped folder for the final submissions.


## Output
The files listed under "Files that are also generated by the code" are the output of the code.

## Sources
- SDG data: https://unstats.un.org/sdgs/unsdg
- Mahalanobis Distance functions: https://stackoverflow.com/questions/46827580/multivariate-outlier-removal-with-mahalanobis-distance
- Population data: https://population.un.org/wpp/Download/Standard/Population/
- Country code data: https://unstats.un.org/unsd/methodology/m49/overview/
