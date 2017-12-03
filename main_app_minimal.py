import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QWidget, QAction, QTabWidget, QVBoxLayout,\
                            QHBoxLayout, QGridLayout, QSplitter, QFrame, QTextEdit, QFileDialog, QGroupBox,\
                            QButtonGroup, QLabel, QRadioButton

from PyQt5 import QtGui
from PyQt5 import QtCore

import pandas as pd

# import my own implementation of stuff
from MyWidgets import MyRadioButtonGroup, MatplotlibFigure

class App(QMainWindow):
    """ This creates the main Window and configures its look
    """
    def __init__(self):
        '''
        Initializes the class with standard parameters
        '''
        super().__init__()
        self.title = 'Online Monitoring Data Analysis App'

        # start at top left corner of the screen
        self.left = 0
        self.top = 0

        # set the window height and width
        self.width = 1280
        self.height = 780

        # set the styles of fonts etc.
        self.setStyleSheet('font-size: 16pt')

        # call the makeUI method
        self.makeUI()

    def makeUI(self):
        # set window geometry
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # generate the tab layout
        self.table_widget = MyTableWidget(self)
        self.setCentralWidget(self.table_widget)

        # apparently we have to call the show method in order to show it
        self.show()


class MyTableWidget(QWidget):
    """
    Initializes the tab layout
    """

    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)

        # initialize the tab screens
        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()
        self.tab4 = QWidget()



        # add the tab screens to the tab widget
        self.tabs.resize(600, 600)
        self.tabs.addTab(self.tab1, 'Get Data Module')
        self.tabs.addTab(self.tab2, 'AT-FTIR Baseline Correction Module')
        self.tabs.addTab(self.tab3, 'AT-FTIR Pattern Over Time')
        self.tabs.addTab(self.tab4, 'AT-FTIR Endpoint analysis')

        # make the layout of the tabs
        self.make_ui_tab1()

        # initialize the tabs
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

    def make_ui_tab1(self):
        """Style of tab 1 is created here"""

        '''Defines master layout of tab1'''
        self.tab1.layout = QHBoxLayout()

        '''Button Section'''
        # folder open button
        btn_open = QPushButton('Open File')
        btn_open.clicked.connect(self.open)
        #btn_open.move(0, 0)

        # check if data is in correct form
        btn_check_data = QPushButton('Check validity of data')
        btn_check_data.clicked.connect(self.check_data)
        #btn_subtract_baseline.move(0, 0)

        # converts the data into excel and pandas dataframe
        btn_plot_data = QPushButton('Plot data')
        btn_plot_data.clicked.connect(self.plot_data)

        # converts the data into excel and pandas dataframe
        btn_data_parser = QPushButton('Extract data')
        btn_data_parser.clicked.connect(self.data_parser)

        '''Button layout section'''
        btn_layout = QVBoxLayout()
        btn_layout.addWidget(btn_open)
        btn_layout.addWidget(btn_check_data)
        btn_layout.addWidget(btn_plot_data)
        btn_layout.addWidget(btn_data_parser)
        btn_layout.addStretch(1)

        radio_buttons = MyRadioButtonGroup('All imported experiments:',
                                           'Select experiments to analyze',
                                           ['A', 'B', 'C'])

        '''Page layout section '''

        topleft = QFrame()
        #topleft.setStyleSheet("border:1px solid rgb(0, 255, 0); ")
        topleft.setLayout(btn_layout)

        self.figure = MatplotlibFigure()

        bottom = QFrame()
        bottom.setFrameShape(QFrame.StyledPanel)

        splitter1 = QSplitter(QtCore.Qt.Horizontal)
        splitter1.addWidget(topleft)
        splitter1.addWidget(self.figure)
        splitter1.addWidget(radio_buttons)

        splitter1.setSizes([5, 400, 5])


        splitter_main = QSplitter(QtCore.Qt.Vertical)
        splitter_main.addWidget(splitter1)
        splitter_main.addWidget(bottom)
        splitter_main.setSizes([200, 20])


        # add the last splitter to the layout
        self.tab1.layout.addWidget(splitter_main)
        self.tab1.setLayout(self.tab1.layout)

    '''
    Methods linked to buttons
    
    These are the methods linked to the buttons in the layout. The functions can call other functions defined in 
    the next section    '''
    def show_data(self):
        """
        This function shows the pandas dataframe in self.XXXX
        https://stackoverflow.com/questions/44603119/how-to-display-a-pandas-data-frame-with-pyqt5/44605011#44605011
        :return:
        """
        path = None
        df = pd.read_csv(path)
        model = PandasModel(df)
        self.tableView.setModel(model)

    def open(self):
        """
        Creates the open folder dialog
        :return: None
        """
        self.open_file()

    def check_data(self):
        """
        Checks if data is in correct form (as defined by Specs elsewhere)
        :return: None
        """
        pass

    def data_parser(self):
        """
        Calls the get_data.py function
        :return: None
        """
        pass

    def plot_data(self):
        self.figure.plot()

    ''' Methods called by buttons 
        These are the methods called by the button methods
    '''

    def open_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getOpenFileName(self, 'QFileDialog.getOpenFileName()',
                                                   '',
                                                   'All Files (*);;Python Files (*.py)',
                                                   options=options)
        # check for valid data could be included here
        if file_name:
            print(file_name)


if __name__ == '__main__':
    """ This code block is always the same and makes sure that e.g. STRG+C kills the window etc.
    """
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec())

