from PyQt5 import QtCore, QtGui, QtWidgets
import quandl, math
import numpy as np
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
from matplotlib import style
import datetime

class Ui_select_graph(QtWidgets.QMainWindow):
    def setupUi(self, MainWindow,svar):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.svar=svar
        MainWindow.setStyleSheet("background-image: url(:/newPrefix/image.jpg);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(280, 200, 271, 211))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.predictedadjclose_pushButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.predictedadjclose_pushButton.setStyleSheet("font: 16pt \"Ubuntu Condensed\";\n"
"color: rgb(255, 255, 255);\n"
"")
        self.predictedadjclose_pushButton.setObjectName("predictedadjclose_pushButton")
        self.predictedadjclose_pushButton.clicked.connect(self.plot)
        self.verticalLayout.addWidget(self.predictedadjclose_pushButton)
        self.adjopenvsadjclose_pushButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.adjopenvsadjclose_pushButton.setStyleSheet("font: 16pt \"Ubuntu Condensed\";\n"
"color: rgb(255, 255, 255);\n"
"")
        self.adjopenvsadjclose_pushButton.setObjectName("adjopenvsadjclose_pushButton")
        self.adjopenvsadjclose_pushButton.clicked.connect(self.openclose)
        self.verticalLayout.addWidget(self.adjopenvsadjclose_pushButton)
        self.highvslow_pushButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.highvslow_pushButton.setStyleSheet("font: 16pt \"Ubuntu Condensed\";\n"
"color: rgb(255, 255, 255);\n"
"")
        self.highvslow_pushButton.setObjectName("highvslow_pushButton")
        self.highvslow_pushButton.clicked.connect(self.highlow)
        self.verticalLayout.addWidget(self.highvslow_pushButton)
        self.volume_pushButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.volume_pushButton.setStyleSheet("font: 16pt \"Ubuntu Condensed\";\n"
"color: rgb(255, 255, 255);\n"
"")
        self.volume_pushButton.setObjectName("volume_pushButton")
        self.volume_pushButton.clicked.connect(self.volume)
        self.verticalLayout.addWidget(self.volume_pushButton)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(160, 40, 481, 51))
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
        self.predictedadjclose_pushButton.setText(_translate("MainWindow", "Predicted Adj. Close"))
        self.adjopenvsadjclose_pushButton.setText(_translate("MainWindow", "Adj.Open vs Adj.Close"))
        self.highvslow_pushButton.setText(_translate("MainWindow", "High vs Low"))
        self.volume_pushButton.setText(_translate("MainWindow", "Volume"))
        self.label.setText(_translate("MainWindow", "Select a graph to plot"))

    def plot(self):
        style.use('ggplot')
        quandl.ApiConfig.api_key = "dJtR145iLysnL9EneYhb"
        df = quandl.get('WIKI' + self.svar)
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

        df['Adj. Close'].plot()

        df['Forecast'].plot()

        plt.legend(loc=4)

        plt.xlabel('Date')

        plt.ylabel('Price')

        plt.show()

    def openclose(self):
        style.use('ggplot')
        quandl.ApiConfig.api_key = "dJtR145iLysnL9EneYhb"
        df = quandl.get('WIKI' + self.svar)
        df = df[['Adj. Open', 'Adj. High', 'Adj. Low', 'Adj. Close', 'Adj. Volume']]
        df['PCT_change'] = (df['Adj. Close'] - df['Adj. Open']) / df['Adj. Open'] * 100.0
        df = df[['Adj. Close', 'PCT_change', 'Adj. Volume']]
        df['PCT_change'].plot()
        plt.xlabel('Date')
        plt.ylabel('% change between Adj. Open and Adj. Close')
        plt.show()

    def highlow(self):
        style.use('ggplot')
        quandl.ApiConfig.api_key = "dJtR145iLysnL9EneYhb"
        df = quandl.get('WIKI' + self.svar)
        df = df[['Adj. Open', 'Adj. High', 'Adj. Low', 'Adj. Close', 'Adj. Volume']]
        df['HL_PCT'] = (df['Adj. High'] - df['Adj. Low']) / df['Adj. Low'] * 100.0
        df = df[['Adj. Close', 'HL_PCT', 'Adj. Volume']]
        df['HL_PCT'].plot()
        plt.xlabel('Date')
        plt.ylabel('% change between Adj. High and Adj. Low')
        plt.show()

    def volume(self):
        style.use('ggplot')
        quandl.ApiConfig.api_key = "dJtR145iLysnL9EneYhb"
        df = quandl.get('WIKI' + self.svar)
        df = df[['Adj. Open', 'Adj. High', 'Adj. Low', 'Adj. Close', 'Adj. Volume']]
        df = df[['Adj. Close', 'Adj. Volume']]
        df['Adj. Volume'].plot()
        plt.xlabel('Date')
        plt.ylabel('Volume of shares transacted')
        plt.show()
import image_rc
