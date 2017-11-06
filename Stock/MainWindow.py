from PyQt5 import QtCore, QtGui, QtWidgets
import quandl, math
import numpy as np
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from matplotlib import style
import datetime
svar = ""

class Ui_MainWindow(QtWidgets.QMainWindow):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        MainWindow.setStyleSheet("background-image: url(:/newPrefix/image.jpg);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(290, 150, 191, 188))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.Google_radioButton = QtWidgets.QRadioButton(self.verticalLayoutWidget)
        self.Google_radioButton.setAutoFillBackground(False)
        self.Google_radioButton.setStyleSheet("font: 14pt \"Ubuntu Condensed\";\n"
"color: rgb(255, 255, 255);")
        self.Google_radioButton.setObjectName("Google_radioButton")
        self.verticalLayout.addWidget(self.Google_radioButton)
        self.Microsoft_radioButton = QtWidgets.QRadioButton(self.verticalLayoutWidget)
        self.Microsoft_radioButton.setStyleSheet("font: 14pt \"Ubuntu Condensed\";\n"
"color: rgb(255, 255, 255);")
        self.Microsoft_radioButton.setObjectName("Microsoft_radioButton")
        self.verticalLayout.addWidget(self.Microsoft_radioButton)
        self.Tesla_radioButton = QtWidgets.QRadioButton(self.verticalLayoutWidget)
        self.Tesla_radioButton.setStyleSheet("font: 14pt \"Ubuntu Condensed\";\n"
"color: rgb(255, 255, 255);")
        self.Tesla_radioButton.setObjectName("Tesla_radioButton")
        self.verticalLayout.addWidget(self.Tesla_radioButton)
        self.Twitter_radioButton = QtWidgets.QRadioButton(self.verticalLayoutWidget)
        self.Twitter_radioButton.setStyleSheet("font: 14pt \"Ubuntu Condensed\";\n"
"color: rgb(255, 255, 255);")
        self.Twitter_radioButton.setObjectName("Twitter_radioButton")
        self.verticalLayout.addWidget(self.Twitter_radioButton)
        self.Facebook_radioButton = QtWidgets.QRadioButton(self.verticalLayoutWidget)
        self.Facebook_radioButton.setStyleSheet("font: 14pt \"Ubuntu Condensed\";\n"
"color: rgb(255, 255, 255);")
        self.Facebook_radioButton.setObjectName("Facebook_radioButton")
        self.verticalLayout.addWidget(self.Facebook_radioButton)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(140, 20, 481, 51))
        font = QtGui.QFont()
        font.setFamily("Ubuntu Condensed")
        font.setPointSize(28)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label.setFont(font)
        self.label.setStyleSheet("font: 28pt \"Ubuntu Condensed\";\n"
"border-color: rgb(255, 0, 0);\n"
"color: rgb(255, 255, 255);")
        self.label.setFrameShadow(QtWidgets.QFrame.Plain)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(110, 410, 551, 30))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.createcsv_pushButton = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.createcsv_pushButton.setStyleSheet("font: 16pt \"Ubuntu Condensed\";\n"
"color: rgb(255, 255, 255);\n"
"")
        self.createcsv_pushButton.setObjectName("createcsv_pushButton")
        self.createcsv_pushButton.clicked.connect(self.createcsv)
        self.horizontalLayout.addWidget(self.createcsv_pushButton)
        self.plotdata_pushButton = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.plotdata_pushButton.setStyleSheet("font: 16pt \"Ubuntu Condensed\";\n"
"color: rgb(255, 255, 255);")
        self.plotdata_pushButton.setObjectName("plotdata_pushButton")
        self.plotdata_pushButton.clicked.connect(self.selectgraph)
        self.horizontalLayout.addWidget(self.plotdata_pushButton)
        self.verticalLayoutWidget.raise_()
        self.horizontalLayoutWidget.raise_()
        self.label.raise_()
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 19))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.Google_radioButton.setText(_translate("MainWindow", "Google"))
        self.Microsoft_radioButton.setText(_translate("MainWindow", "Microsoft"))
        self.Tesla_radioButton.setText(_translate("MainWindow", "Tesla"))
        self.Twitter_radioButton.setText(_translate("MainWindow", "Twitter"))
        self.Facebook_radioButton.setText(_translate("MainWindow", "Facebook"))
        self.label.setText(_translate("MainWindow", "Stock Market Prediction System"))
        self.createcsv_pushButton.setText(_translate("MainWindow", "Create csv output file"))
        self.plotdata_pushButton.setText(_translate("MainWindow", "Plot data"))

    def choose(self):
        svar=""
        if self.Google_radioButton.isChecked():
            svar = '/GOOGL'
        elif self.Microsoft_radioButton.isChecked():
            svar = '/MSFT'
        elif self.Tesla_radioButton.isChecked():
            svar = '/TSLA'
        elif self.Twitter_radioButton.isChecked():
            svar = '/TWTR'
        elif self.Facebook_radioButton.isChecked():
            svar = '/FB'
        else:
            msg = QtWidgets.QMessageBox()
            msg.setWindowTitle("Error")
            msg.setText("Please select a company")
            msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
            retval = msg.exec_()
            return
        return svar

    def createcsv(self):

        if self.Google_radioButton.isChecked():
            svar = 'GOOGL'
        elif self.Microsoft_radioButton.isChecked():
            svar = 'MSFT'
        elif self.Tesla_radioButton.isChecked():
            svar = 'TSLA'
        elif self.Twitter_radioButton.isChecked():
            svar = 'TWTR'
        elif self.Facebook_radioButton.isChecked():
            svar = 'FB'
        else:
            msg = QtWidgets.QMessageBox()
            msg.setWindowTitle("Error")
            msg.setText("Please select a company")
            msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
            retval = msg.exec_()
            return
        style.use('ggplot')
        quandl.ApiConfig.api_key = "dJtR145iLysnL9EneYhb"
        df = quandl.get('WIKI/' + svar)
        df = df[['Adj. Open', 'Adj. High', 'Adj. Low', 'Adj. Close', 'Adj. Volume']]
        df['HL_PCT'] = (df['Adj. High'] - df['Adj. Low']) / df['Adj. Close'] * 100.0
        df['PCT_change'] = (df['Adj. Close'] - df['Adj. Open']) / df['Adj. Open'] * 100.0
        df = df[['Adj. Close', 'HL_PCT', 'PCT_change', 'Adj. Volume']]
        forecast_col = 'Adj. Close'
        df.fillna(value=-99999, inplace=True)
        forecast_out = int(math.ceil(0.01 * len(df)))
        df['label'] = df[forecast_col].shift(-forecast_out)
        X = np.array(df.drop(['label'], 1))
        X = preprocessing.scale(X)
        X_lately = X[-forecast_out:]
        X = X[:-forecast_out]
        df.dropna(inplace=True)
        y = np.array(df['label'])
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
        clf = LinearRegression(n_jobs=-1)
        clf.fit(X_train, y_train)
        confidence = clf.score(X_test, y_test)
        forecast_set = clf.predict(X_lately)
        df['Forecast'] = np.nan
        last_date = df.iloc[-1].name
        last_unix = last_date.timestamp()
        one_day = 86400
        next_unix = last_unix + one_day

        for i in forecast_set:
            next_date = datetime.datetime.fromtimestamp(next_unix)

            next_unix += 86400

            df.loc[next_date] = [np.nan for _ in range(len(df.columns) - 1)] + [i]

        df.to_csv(svar+'.csv')

        msg=QtWidgets.QMessageBox()
        msg.setWindowTitle("Success")
        msg.setText("Successfully created csv")
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
        retval=msg.exec_()

    def selectgraph(self):
        from select_graph import Ui_select_graph
        svar=self.choose()
        if svar==None:
            return
        self.selectgraph = QtWidgets.QMainWindow()
        self.ui = Ui_select_graph()
        self.ui.setupUi(self.selectgraph,svar)
        self.selectgraph.show()

import image_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

