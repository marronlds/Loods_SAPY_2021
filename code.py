# Radio button that will give you the outcome of the Lilliefors normality test.
# based on this outcome you can decide between using the Spearman Rank test, or the Pearson correlation test
# After making the decision, the correlation statistic and p-value will be given
# plus an interpretation of this.


from PyQt5 import QtCore, QtGui, QtWidgets
import SAPYfunctions as sapy


# Making the layout of the  widget
class Ui_MainWindow(QtWidgets.QMainWindow):
    """ The class of the GUI is created.  """
    def setupUi(self, MainWindow, lilliefors_df, correlation_df):
        """ Setting up de GUI. The GUI gives the result of the Lilliefors normality test. Then you can decide whether to perform a Pearson or a Spearman correlation test. It subsequently gives the outcome of the correlation test. When you press 'select test', that correlation test is used in the rest of the code. To close press X.
        
        Args: 
            MainWindow
            lilliefors_df (DataFrame): the dataframe of the lilliefors results
            correlation_df (DataFrame): the dataframe of the pearson and spearman correlation results
            
        Returns:
            A GUI which gives the outcome of the normality test, which allows you to choose between the Spearman test or the Pearson test.
            
        """
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(597, 717)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        # radio button 1 (Pearson)
        self.radioButton = QtWidgets.QRadioButton(self.centralwidget)
        self.radioButton.setGeometry(QtCore.QRect(200, 230, 231, 20))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.radioButton.setFont(font)
        self.radioButton.setObjectName("radioButton")
        # radio button 2 (Spearman)
        self.radioButton_2 = QtWidgets.QRadioButton(self.centralwidget)
        self.radioButton_2.setGeometry(QtCore.QRect(200, 270, 231, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.radioButton_2.setFont(font)
        self.radioButton_2.setObjectName("radioButton_2")
        # Push button
        self.pushButton = QtWidgets.QPushButton(self.centralwidget, clicked = lambda: self.select(correlation_df))
        self.pushButton.setGeometry(QtCore.QRect(170, 320, 181, 28))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        # labels
        self.label_i = QtWidgets.QLabel(self.centralwidget)
        self.label_i.setGeometry(QtCore.QRect(10, 420, 531, 16))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_i.setFont(font)
        self.label_i.setObjectName("label_i")
        self.label_j = QtWidgets.QLabel(self.centralwidget)
        self.label_j.setGeometry(QtCore.QRect(10, 450, 501, 41))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_j.setFont(font)
        self.label_j.setObjectName("label_j")
        self.label_a = QtWidgets.QLabel(self.centralwidget)
        self.label_a.setGeometry(QtCore.QRect(170, 0, 221, 31))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_a.setFont(font)
        self.label_a.setObjectName("label_a")
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(0, 360, 521, 16))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.line.setFont(font)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.line_2 = QtWidgets.QFrame(self.centralwidget)
        self.line_2.setGeometry(QtCore.QRect(0, 150, 521, 20))
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.label_b = QtWidgets.QLabel(self.centralwidget)
        self.label_b.setGeometry(QtCore.QRect(120, 30, 51, 41))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setItalic(True)
        self.label_b.setFont(font)
        self.label_b.setObjectName("label_b")
        self.label_h = QtWidgets.QLabel(self.centralwidget)
        self.label_h.setGeometry(QtCore.QRect(140, 180, 311, 16))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setItalic(True)
        self.label_h.setFont(font)
        self.label_h.setObjectName("label_h")
        self.label_l = QtWidgets.QLabel(self.centralwidget)
        self.label_l.setGeometry(QtCore.QRect(10, 550, 571, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_l.setFont(font)
        self.label_l.setObjectName("label_l")
        self.label_k = QtWidgets.QLabel(self.centralwidget)
        self.label_k.setGeometry(QtCore.QRect(10, 510, 541, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_k.setFont(font)
        self.label_k.setObjectName("label_k")
        self.label_d = QtWidgets.QLabel(self.centralwidget)
        self.label_d.setGeometry(QtCore.QRect(110, 70, 191, 16))
        self.label_d.setObjectName("label_d")
        self.label_f = QtWidgets.QLabel(self.centralwidget)
        self.label_f.setGeometry(QtCore.QRect(110, 100, 211, 16))
        self.label_f.setObjectName("label_f")
        self.label_g = QtWidgets.QLabel(self.centralwidget)
        self.label_g.setGeometry(QtCore.QRect(360, 100, 221, 16))
        self.label_g.setObjectName("label_g")
        self.label_c = QtWidgets.QLabel(self.centralwidget)
        self.label_c.setGeometry(QtCore.QRect(370, 30, 51, 41))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setItalic(True)
        self.label_c.setFont(font)
        self.label_c.setObjectName("label_c")
        self.label_e = QtWidgets.QLabel(self.centralwidget)
        self.label_e.setGeometry(QtCore.QRect(360, 70, 221, 16))
        self.label_e.setObjectName("label_e")
        # push button 2
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget, clicked = lambda: self.select_2())
        self.pushButton_2.setGeometry(QtCore.QRect(170, 620, 181, 28))
        font = QtGui.QFont() 
        font.setPointSize(12)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setObjectName("pushButton_2")
        
        # menubar and statusbar
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 597, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow, lilliefors_df)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

         #giving text to the labels.
         #calling in th
    def retranslateUi(self, MainWindow, lilliefors_df):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.radioButton.setText(_translate("MainWindow", "Pearson"))
        self.radioButton_2.setText(_translate("MainWindow", "Spearman"))
        self.pushButton.setText(_translate("MainWindow", "See test outcome"))
        
        self.label_a.setText(_translate("MainWindow", "Lilliefors test for normality"))
        self.label_b.setText(_translate("MainWindow", "SDG 5"))
        self.label_h.setText(_translate("MainWindow", "Choose correlation test statistic:"))
        self.label_d.setText(_translate("MainWindow", "D-statistic: {} ".format(round(lilliefors_df.iloc[0]['D'],3))))
        self.label_f.setText(_translate("MainWindow", "p-value: {}".format(lilliefors_df.iloc[0]['p'])))
        self.label_g.setText(_translate("MainWindow", "p-value: {} ".format(lilliefors_df.iloc[0]['p'])))
        self.label_c.setText(_translate("MainWindow", "SDG 12"))
        self.label_e.setText(_translate("MainWindow", "D-statistic:{} ".format(lilliefors_df.iloc[1]['D'])))

        # Giving text to the labels, depending on which button is selected
    def select(self, correlation_df):
        _translate = QtCore.QCoreApplication.translate
        if self.radioButton.isChecked():
            self.pushButton_2.setText(_translate("MainWindow", "Select test"))
            self.label_i.setText(_translate("MainWindow", "Correlation coefficient: {}".format(correlation_df.iloc[0]['correlation'])))
            self.label_j.setText(_translate("MainWindow", "p-value: {}".format(correlation_df.iloc[0]['p'])))
            self.label_l.setText(_translate("MainWindow", str(sapy.correlation_significance(correlation_df, 'Pearson'))))
            self.label_k.setText(_translate("MainWindow", str(sapy.correlation_direction(correlation_df, 'Pearson'))))
        elif self.radioButton_2.isChecked():
            self.pushButton_2.setText(_translate("MainWindow", "Select test"))
            self.label_i.setText(_translate("MainWindow", "Correlation coefficient: {}".format(correlation_df.iloc[1]['correlation'])))
            self.label_j.setText(_translate("MainWindow", "p-value: {}".format(correlation_df.iloc[1]['p'])))
            self.label_l.setText(_translate("MainWindow", str(sapy.correlation_significance(correlation_df, 'Spearman'))))
            self.label_k.setText(_translate("MainWindow", str(sapy.correlation_direction(correlation_df, 'Spearman'))))



#### If button 2 is selected, I want global variables to be created and to close the widget.
    def select_2(self):
        if self.radioButton.isChecked():  
           self.correlation_test = 'Pearson'
           self.correlation_loc = 0
 #          self.test = 'Als hij dit print dan gaat de info van Radio naar txt'

           
        if self.radioButton_2.isChecked():
            self.correlation_test = 'Spearman'
            self.correlation_loc = 1
 #           self.test = 'Als hij dit print dan gaat de info van Radio naar txt'

