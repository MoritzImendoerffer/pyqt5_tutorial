import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QWidget, QAction, QTabWidget, QVBoxLayout,\
                            QHBoxLayout, QGridLayout, QSplitter, QFrame, QTextEdit, QFileDialog, QGroupBox,\
                            QButtonGroup, QLabel, QRadioButton

from PyQt5 import QtCore

import matplotlib
from matplotlib import figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

class MatplotlibFigure(QWidget):

    # constructor
    def __init__(self):
        super().__init__()
        #self.layout = QBoxLayout()
        self.figure = matplotlib.figure.Figure()
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setParent(self)
        self.toolbar = NavigationToolbar(self.canvas, self)
        #self.layout.addWidget(self.canvas)

    def plot(self):
        self.figure.clf()
        ax = self.figure.add_subplot(111)
        x = [i for i in range(100)]
        y = [i**0.5 for i in x]
        ax.plot(x, y, 'g*-')
        self.canvas.draw_idle()
        print('PLOTTED')


class MainApp(QMainWindow):
    """ This creates the main Window and configures its look
    """
    def __init__(self):
        '''
        Initializes the class with standard parameters
        '''
        super().__init__()
        self.title = 'Data Analysis App'

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
        self.table_widget = MyTableWidget()
        self.setCentralWidget(self.table_widget)

        # apparently we have to call the show method in order to show it
        self.show()

class MyTableWidget(QWidget):
    """
    Initializes the tab layout
    """

    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)

        # initialize the tab screens
        self.tabs = QTabWidget()

        # add the tab screens to the tab widget
        self.tabs.resize(600, 600)

        # make the layout of the tabs
        self.make_tab1()

        # initialize the tabs
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

    def make_tab1(self):
        """Style of tab 1 is created here"""

        '''Defines master layout of tab1'''
        tab1 = QWidget()
        tab1.layout = QHBoxLayout()

        '''Button Section'''

        # converts the data into excel and pandas dataframe
        btn_plot_data = QPushButton('Plot data')
        btn_plot_data.clicked.connect(self.plot_data)


        '''Button layout section'''
        btn_layout = QVBoxLayout()
        btn_layout.addWidget(btn_plot_data)
        btn_layout.addStretch(1)

        '''Page layout section '''


        left = QFrame()
        #btn_layout.addWidget(self.figure.toolbar)
        left.setLayout(btn_layout)

        # combine the buttons and the canvas in a splitter layout
        splitter1 = QSplitter(QtCore.Qt.Horizontal)
        splitter1.addWidget(left)
        self.figure = MatplotlibFigure()
        splitter1.addWidget(self.figure)
        splitter1.setSizes([5, 400])


        # add the last splitter to the layout
        tab1.layout.addWidget(splitter1)
        tab1.setLayout(tab1.layout)
        self.tabs.addTab(tab1, 'Get Data Module')

    ''' Methods section
    '''
    def plot_data(self):
        self.figure.plot()


if __name__ == '__main__':
    """ This code block is always the same and makes sure that e.g. STRG+C kills the window etc.
    """
    app = QApplication(sys.argv)
    ex = MainApp()
    sys.exit(app.exec())

