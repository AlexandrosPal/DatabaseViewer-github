from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog, QHeaderView
import sqlite3


# main class
class Ui_mainWindow(object):
    def setupUi(self, mainWindow):
        mainWindow.setObjectName("mainWindow")
        mainWindow.resize(466, 518)
        self.centralwidget = QtWidgets.QWidget(mainWindow)
        self.centralwidget.setObjectName("centralwidget")
        
        # table widget set-up
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(30, 210, 411, 241))
        self.tableWidget.setStyleSheet("")
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)


        # search in db button
        self.searchDb = QtWidgets.QPushButton(self.centralwidget)
        self.searchDb.setGeometry(QtCore.QRect(290, 460, 151, 31))
        self.searchDb.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.searchDb.setObjectName("searchDb")

        # search bar widget
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(30, 460, 141, 31))
        self.lineEdit.setObjectName("lineEdit")


        # select file button
        self.selectFile = QtWidgets.QPushButton(self.centralwidget, clicked = lambda: self.selectDatabase(self.databaseLabel, self.comboBox, self.tableLabel))
        self.selectFile.setGeometry(QtCore.QRect(30, 20, 221, 71))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.selectFile.setFont(font)
        self.selectFile.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.selectFile.setMouseTracking(False)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("../Assets/opendb.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.selectFile.setIcon(icon1)
        self.selectFile.setIconSize(QtCore.QSize(30, 30))
        self.selectFile.setCheckable(False)
        self.selectFile.setObjectName("selectFile")


        # select table widget
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(30, 100, 221, 22))
        self.comboBox.setObjectName("comboBox")


        # view selected db and table
        self.gobutton = QtWidgets.QPushButton(self.centralwidget)
        self.gobutton.setGeometry(QtCore.QRect(30, 130, 401, 23))
        self.gobutton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.gobutton.setObjectName("gobutton")


        # Show select db label
        self.databaseLabel = QtWidgets.QLabel(self.centralwidget)
        self.databaseLabel.setGeometry(QtCore.QRect(260, 30, 161, 16))
        self.databaseLabel.setObjectName("databaseLabel")


        # Show select table label
        self.tableLabel = QtWidgets.QLabel(self.centralwidget)
        self.tableLabel.setGeometry(QtCore.QRect(260, 100, 171, 16))
        self.tableLabel.setObjectName("tableLabel")
        mainWindow.setCentralWidget(self.centralwidget)

        
        # window name
        self.statusbar = QtWidgets.QStatusBar(mainWindow)
        self.statusbar.setObjectName("statusbar")
        mainWindow.setStatusBar(self.statusbar)


        # call renaming function
        self.retranslateUi(mainWindow)
        QtCore.QMetaObject.connectSlotsByName(mainWindow)


    def selectDatabase(self, dblabel, comboBox, tableLabel):
        # open file dialog
        fname = QFileDialog.getOpenFileName(None, "Select a file", '', "Database Files (*.db)", options=QFileDialog.DontUseNativeDialog)
        
        # get path
        path = fname[0]
        
        # save path to .txt file
        with open("path.txt", 'w') as f:
            f.write(path)
        
        # set label to db name
        dbName = path.split('/')[-1]
        dblabel.setText(dbName)
        
        # sqlite connection
        conn = sqlite3.connect(path)
        c = conn.cursor()

        # get all tables
        tables = []
        c.execute(f"SELECT name FROM sqlite_master WHERE type='table';")
        tables_raw = c.fetchall()
        for table in tables_raw:
            tables.append(table[0])

        # fill table combobox
        comboBox.clear()
        comboBox.addItems(tables)

        # change table label
        tableLabel.setText(str(comboBox.currentText()))
        comboBox.currentIndexChanged.connect(lambda: tableLabel.setText(str(comboBox.currentText())))
                            

    # renaming function of pyqt5
    def retranslateUi(self, mainWindow):
        _translate = QtCore.QCoreApplication.translate
        mainWindow.setWindowTitle(_translate("mainWindow", "Database Viewer"))
        self.searchDb.setText(_translate("mainWindow", "Search Database"))
        self.lineEdit.setText(_translate("mainWindow", "Search in Database"))
        self.selectFile.setText(_translate("mainWindow", "Open Database"))
        self.gobutton.setText(_translate("mainWindow", "Go!"))
        self.databaseLabel.setText(_translate("mainWindow", "No file selected."))
        self.tableLabel.setText(_translate("mainWindow", "No table selected."))


# initialize window
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = QtWidgets.QMainWindow()
    ui = Ui_mainWindow()
    ui.setupUi(mainWindow)
    mainWindow.show()
    sys.exit(app.exec_())