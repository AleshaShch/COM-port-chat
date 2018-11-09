import sys
import serial
import threading
import time
from PyQt5 import QtWidgets, QtCore
import view
import com_port


class MainWindow(QtWidgets.QMainWindow, view.Ui_MainWindow):
    MISTAKE_FLAG = 1
    MESSAGE_WITHOUT_MISTAKE = 0

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.port = None
        self.thread_read = None
        self.data = None
        self.fl = threading.Event
        self.pushButton_send.clicked.connect(self.send)
        self.pushButton_connect.clicked.connect(self.connect)
        self.pushButton_disconnect.clicked.connect(self.disconnect)

    def set_daemon_thread(self, target):
        self.thread_read = threading.Thread(target=target)
        self.thread_read.daemon = True
        self.thread_read.start()

    def output_data(self):
        while self.port.serial.is_open:
            self.fl.wait
            self.textEdit.setText('{}\n'.format(self.data))
            self.fl.clear

    def connect(self):
        port_name = str(self.comboBox_connection.itemText(self.comboBox_connection.currentIndex()))
        baudrate = str(self.comboBox_baudrate.itemText(self.comboBox_baudrate.currentIndex()))
        try:
            self.port = com_port.ComPort(port_name, baudrate)
        except serial.SerialException as e:
            sys.stderr.write('Could not open serial port {}: {}\n'.format(port_name, e))
            self.textEdit.setText('Could not open serial port {}\n'.format(port_name))
            return -1
        self.textEdit.setText('Connect to {}\n'.format(port_name))
        self.set_daemon_thread(self.display_data)

    def send(self):
        try:
            if self.checkBox_mistake.isChecked():
                self.port.write_frame(self.lineEdit.displayText().encode("utf-8", errors="ignore"), self.MISTAKE_FLAG)
            else:
                self.port.write_frame(self.lineEdit.displayText().encode("utf-8", errors="ignore"), self.MESSAGE_WITHOUT_MISTAKE)
        except serial.SerialException as e:
            self.textEdit('Write error\n')

    def display_data(self):
        while self.port.serial.is_open:
            time.sleep(0.1)
            text = self.port.read_data_without_flag()
            if text:
                print(''.join(text))


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()


if __name__ == "__main__":
    main()



