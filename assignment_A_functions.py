# -*- coding: utf-8 -*-
"""

Course:         Sustainability Analysis in Python
Author:         Marron Loods
Coordinator:    Laura Scherer
Date:           November 9, 2021

This file contains the functions which accompany the assignment.py code.

"""

#%% Imports

import numpy as np
from PyQt5.QtWidgets import (QLabel, QRadioButton, QVBoxLayout, QWidget)
from PyQt5 import QtCore
from scipy import stats


#%% Significance

# The function takes a list of a boolean which indicates whether the 
# test should be parametric or not. If so, Pearon's test is performed, 
# otherwise Spearman's test is performed.


def significance(test_result):
    """ Significance indicator
    
    Indicates whether the results of a statistical test are significant.
    
    Args:
        test_result (tuple):     a dataframe with the different statistical tests in the rows, and the test statistic and p-value in the columns.
    
    Returns:
        String which indicates whether the result is significant based on the p-value.
            If the result is significant, it also returns the level of significance
            If the result is insignificant, it also gives the found p-value
    
    Examples:
        >>> test_tuple1 = (0.1339910250281786, 0.0009999999999998899)
        >>> significance(test_tuple1)
        >>> 'The correlation is statistically significant at a level of 0.01.'
        
        >>> test_tuple2 = (0.07731910636894324, 0.21535038152401192)
        >>> significance(test_tuple2)
        >>> 'The correlation is not statistically significant, as the p-value is: 0.2154.'
        
        """ 
        
    if test_result[1] > 0.1:
        return "The correlation is not statistically significant, as the p-value is: " \
            + str(round(test_result[1], 4)) + "."
    elif test_result[1] > 0.05:
        return "The correlation is statistically significant at a level of 0.1."
    elif test_result[1] > 0.01:
        return "The correlation is statistically significant at a level of 0.05."
    else:
        return "The correlation is statistically significant at a level of 0.01."
    
#%% Mahalanobis Distance functions

def MahalanobisDist(data, verbose=False):
    """ Measures the distance between a point and a distribution of the dataset.
    """
    
    covariance_matrix = np.cov(data, rowvar=False)
    if is_pos_def(covariance_matrix):
        inv_covariance_matrix = np.linalg.inv(covariance_matrix)
        if is_pos_def(inv_covariance_matrix):
            vars_mean = []
            for i in range(data.shape[0]):
                vars_mean.append(list(data.mean(axis=0)))
            diff = data - vars_mean
            md = []
            for i in range(len(diff)):
                md.append(np.sqrt(diff[i].dot(inv_covariance_matrix).dot(diff[i])))

            if verbose:
                print("Covariance Matrix:\n {}\n".format(covariance_matrix))
                print("Inverse of Covariance Matrix:\n {}\n".format(inv_covariance_matrix))
                print("Variables Mean Vector:\n {}\n".format(vars_mean))
                print("Variables - Variables Mean Vector:\n {}\n".format(diff))
                print("Mahalanobis Distance:\n {}\n".format(md))
            return md
        else:
            print("Error: Inverse of Covariance Matrix is not positive definite!")
    else:
        print("Error: Covariance Matrix is not positive definite!")


def MD_detectOutliers(data, extreme=False, verbose=False):
    """ Detects outliers: datapoints outside of the datacloud determined with
    the Mahalanobis distance and standard deviation.
    """
    MD = MahalanobisDist(data, verbose)

    # According to the 68–95–99.7 rule
    std = np.std(MD)
    k = 3. * std if extreme else 2. * std
    m = np.mean(MD)
    up_t = m + k
    low_t = m - k
    outliers = []
    for i in range(len(MD)):
        if (MD[i] >= up_t) or (MD[i] <= low_t):
            outliers.append(i)  # index of the outlier
    return np.array(outliers)


def is_pos_def(A):
    """Test whether matrix of data and its inverse are Positive Definite."""
    if np.allclose(A, A.T):
        try:
            np.linalg.cholesky(A)
            return True
        except np.linalg.LinAlgError:
            return False
    else:
        return False
    
    
#%% Correlation test    

# The function takes a boolean which indicates
# whether a parametric test should be used. If True, the pearson's R correlation
# coefficient is calculated, if False, the Spearman's R test is used.


def correlation_test(parametric_bool, goal5_data, goal7_data):
    """ Pearson or Spearman correlation test
    
    Performs the Pearson or Spearman correlation test, depending on whether the test should be parametric.
    
    Args:
        parametric_bool (boolean): boolean which indicates whether a parametric test should be used
        goal5_data (Series): Column of dataframe with goal 5 data
        goal7_data (Series): Column of dataframe with goal 7 data
    Returns:
        Tuple with test results
 
    """
    if parametric_bool:
        return stats.pearsonr(goal5_data, goal7_data)
    else:
        return stats.spearmanr(goal5_data, goal7_data)
    
#%% Target reached

# The function takes a row in a dataframe, returns the mean of the two goals
# A target is met when the score is above the mean of all selected countries.

def target_reached(row):
    """ Indicator of targets met
    
    Indicates whether countries have reached one, both, or neither of the 
    targets set for the sustainable development goal. The target is in this 
    case considered reached if a country scores higher than the
    mean of all countries in the dataset.
    
    Args:
        row(Series): Row of a dataframe with the goal results of a country
                        including the means of both goals
    Returns:
        String (Neither, Goal 5 only, Goal 7 only, or Both)
        
    """
    
    if row['Goal5'] <= row['Goal5 mean'] and row['Goal7'] <= row['Goal7 mean']:
        return "Neither"
    elif row['Goal5'] > row['Goal5 mean'] and row['Goal7'] <= row['Goal7 mean']:
        return "Goal 5 only"
    elif row['Goal5'] <= row['Goal5 mean'] and row['Goal7'] > row['Goal7 mean']:
        return "Goal 7 only"
    elif row['Goal5'] > row['Goal5 mean'] and row['Goal7'] > row['Goal7 mean']:
        return "Both"
    else:
        return "No data"
    
#%%


class SelectCoefficient(QWidget):

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        # Make labels and buttons
        self.label = QLabel("Which correlation coefficient do you want to use?")
        self.pearson = QRadioButton("Pearson's R")
        self.spearman = QRadioButton("Spearman's R")
        self.label2 = QLabel("")
        
        # Connect clicking of button to function onClicked
        self.pearson.clicked.connect(self.select)
        self.spearman.clicked.connect(self.select)

        # Create layout of window
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.pearson)
        layout.addWidget(self.spearman)
        layout.addWidget(self.label2)
        
        # Create window
        self.setGeometry(200, 200, 300, 150)
        self.setLayout(layout)
        self.setWindowTitle("Selection of correlation coefficient")
        # Bring to front
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)
        self.show()
        
        
    def select(self):
        radioBtn = self.sender()
        if radioBtn == self.pearson:
            self.parametric_bool = True
        if radioBtn == self.spearman:
            self.parametric_bool = False
        if radioBtn.isChecked():
            self.close()