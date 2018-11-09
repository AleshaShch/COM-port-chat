from PyQt5 import QtWidgets, QtCore


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(300, 400)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 10, 281, 20))
        self.label.setScaledContents(False)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")

        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(10, 250, 171, 51))
        self.lineEdit.setObjectName("lineEdit")

        self.pushButton_send = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_send.setGeometry(QtCore.QRect(180, 260, 91, 28))
        self.pushButton_send.setObjectName("pushButton_send")

        self.splitter = QtWidgets.QSplitter(self.centralwidget)
        self.splitter.setGeometry(QtCore.QRect(10, 40, 277, 192))
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")

        self.textEdit = QtWidgets.QTextEdit(self.splitter)
        self.textEdit.setObjectName("textEdit")
        self.textEdit.setReadOnly(True)

        self.verticalScrollBar = QtWidgets.QScrollBar(self.splitter)
        self.verticalScrollBar.setOrientation(QtCore.Qt.Vertical)
        self.verticalScrollBar.setObjectName("verticalScrollBar")

        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(10, 340, 161, 24))
        self.widget.setObjectName("widget")

        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.comboBox_connection = QtWidgets.QComboBox(self.widget)
        self.comboBox_connection.setEditable(True)
        self.comboBox_connection.setObjectName("comboBox_connection")
        self.comboBox_connection.addItem("COM1")
        self.comboBox_connection.addItem("COM2")
        self.horizontalLayout.addWidget(self.comboBox_connection)

        self.comboBox_baudrate = QtWidgets.QComboBox(self.widget)
        self.comboBox_baudrate.setObjectName("comboBox_baudrate")
        self.comboBox_baudrate.addItem("9600")
        self.comboBox_baudrate.addItem("56625")
        self.comboBox_baudrate.addItem("115200")
        self.horizontalLayout.addWidget(self.comboBox_baudrate)

        self.widget1 = QtWidgets.QWidget(self.centralwidget)
        self.widget1.setGeometry(QtCore.QRect(180, 300, 95, 65))
        self.widget1.setObjectName("widget1")

        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget1)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")

        self.pushButton_connect = QtWidgets.QPushButton(self.widget1)
        self.pushButton_connect.setObjectName("pushButton_connect")
        self.pushButton_connect.setIconSize(QtCore.QSize(20, 20))
        self.verticalLayout.addWidget(self.pushButton_connect)

        self.pushButton_disconnect = QtWidgets.QPushButton(self.widget1)
        self.pushButton_disconnect.setObjectName("pushButton_disconnect")
        self.verticalLayout.addWidget(self.pushButton_disconnect)

        self.layoutWidget_2 = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget_2.setGeometry(QtCore.QRect(10, 310, 161, 24))
        self.layoutWidget_2.setObjectName("layoutWidget_2")

        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.layoutWidget_2)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")

        self.checkBox_mistake = QtWidgets.QCheckBox('Message with mistake', self.layoutWidget_2)
        self.checkBox_mistake.setObjectName("checkBox_mistake")
        self.horizontalLayout_2.addWidget(self.checkBox_mistake)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.retranslateUi(MainWindow)
        self.comboBox_connection.setCurrentIndex(0)
        self.comboBox_baudrate.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "RS-232"))
        self.pushButton_send.setText(_translate("MainWindow", "Send"))
        #self.comboBox_connection.setItemText(0, _translate("MainWindow", "COM1"))
        #self.comboBox_connection.setItemText(1, _translate("MainWindow", "COM2"))
        self.pushButton_connect.setText(_translate("MainWindow", "Connect"))
        self.pushButton_disconnect.setText(_translate("MainWindow", "Disconnect"))