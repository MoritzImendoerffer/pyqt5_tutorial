import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QWidget, QAction, QTabWidget, QVBoxLayout,\
                            QHBoxLayout, QGridLayout, QSplitter, QFrame, QTextEdit

from PyQt5 import QtGui
from PyQt5 import QtCore

import pandas as pd

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
        btn_open = QPushButton('Open Folder')
        btn_open.clicked.connect(self.open_folders)
        #btn_open.move(0, 0)

        # check if data is in correct form
        btn_check_data = QPushButton('Check validity of data')
        btn_check_data.clicked.connect(self.check_data)
        #btn_subtract_baseline.move(0, 0)

        # converts the data into excel and pandas dataframe
        btn_data_parser = QPushButton('Extract data')
        btn_data_parser.clicked.connect(self.data_parser)
        #btn_subtract_baseline.move(0, 0)


        '''Button layout section'''
        btn_layout = QVBoxLayout()
        btn_layout.addWidget(btn_open)
        btn_layout.addWidget(btn_check_data)
        btn_layout.addWidget(btn_data_parser)
        btn_layout.addStretch(1)


        '''Page layout section'''
        topleft = QFrame()
        #topleft.setFrameShape(QFrame.StyledPanel)
        topleft.setLayout(btn_layout)

        bottom = QFrame()
        bottom.setFrameShape(QFrame.StyledPanel)

        splitter1 = QSplitter(QtCore.Qt.Horizontal)

        textedit = QTextEdit()
        splitter1.addWidget(topleft)
        splitter1.addWidget(textedit)
        splitter1.setSizes([20, 200])

        splitter2 = QSplitter(QtCore.Qt.Vertical)
        splitter2.addWidget(splitter1)
        splitter2.addWidget(bottom)


        # add the last splitter to the layout
        self.tab1.layout.addWidget(splitter2)
        self.tab1.setLayout(self.tab1.layout)

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

    def open_folders(self):
        """
        Creates the open folder dialog
        :return: None
        """
        pass

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


class PandasModel(QtCore.QAbstractTableModel):
    """Allows to display pandas dataframe in QT
    https://github.com/eyllanesc/stackoverflow/blob/master/PandasTableView/PandasModel.py
    """
    def __init__(self, df = pd.DataFrame(), parent=None):
        QtCore.QAbstractTableModel.__init__(self, parent=parent)
        self._df = df

    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        if role != QtCore.Qt.DisplayRole:
            return QtCore.QVariant()

        if orientation == QtCore.Qt.Horizontal:
            try:
                return self._df.columns.tolist()[section]
            except (IndexError, ):
                return QtCore.QVariant()
        elif orientation == QtCore.Qt.Vertical:
            try:
                # return self.df.index.tolist()
                return self._df.index.tolist()[section]
            except (IndexError, ):
                return QtCore.QVariant()

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if role != QtCore.Qt.DisplayRole:
            return QtCore.QVariant()

        if not index.isValid():
            return QtCore.QVariant()

        return QtCore.QVariant(str(self._df.ix[index.row(), index.column()]))

    def setData(self, index, value, role):
        row = self._df.index[index.row()]
        col = self._df.columns[index.column()]
        if hasattr(value, 'toPyObject'):
            # PyQt4 gets a QVariant
            value = value.toPyObject()
        else:
            # PySide gets an unicode
            dtype = self._df[col].dtype
            if dtype != object:
                value = None if value == '' else dtype.type(value)
        self._df.set_value(row, col, value)
        return True

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self._df.index)

    def columnCount(self, parent=QtCore.QModelIndex()):
        return len(self._df.columns)

    def sort(self, column, order):
        colname = self._df.columns.tolist()[column]
        self.layoutAboutToBeChanged.emit()
        self._df.sort_values(colname, ascending= order == QtCore.Qt.AscendingOrder, inplace=True)
        self._df.reset_index(inplace=True, drop=True)
        self.layoutChanged.emit()

if __name__ == '__main__':
    """ This code block is always the same and makes sure that e.g. STRG+C kills the window etc.
    """
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec())

