import sys
import serial
import threading
import re
from PyQt5 import QtWidgets
import view
import com_port


class MainWindow(QtWidgets.QMainWindow, view.Ui_MainWindow):
    MISTAKE_FLAG = 1
    MESSAGE_WITHOUT_MISTAKE = 0
    ACTIVE_MONITOR = 1
    SUBSCRIBER = 0

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.station = None
        self.thread_read = None
        self.data = None

        self.pushButton_send.clicked.connect(self.send)
        self.pushButton_connect.clicked.connect(self.connect)
        self.pushButton_disconnect.clicked.connect(self.disconnect)
        self.pushButton_init_ring.clicked.connect(self.init_ring)
        self.pushButton_shutdown.clicked.connect(self.shutdown)

    def connect(self):
        write_port_name = str(self.comboBox_connection.itemText(self.comboBox_connection.currentIndex()))
        mac_address = int(re.findall("\d", write_port_name)[0])
        read_port_name = str(self.comboBox_connection_2.itemText(self.comboBox_connection_2.currentIndex()))
        baudrate = str(self.comboBox_baudrate.itemText(self.comboBox_baudrate.currentIndex()))
        try:
            if self.checkbox_active_station.isChecked():
                self.station = com_port.NetworkStation(write_port_name, read_port_name, baudrate, mac_address,
                                                       monitor_flag=self.ACTIVE_MONITOR)
            else:
                self.station = com_port.NetworkStation(write_port_name, read_port_name, baudrate, mac_address,
                                                        monitor_flag=self.SUBSCRIBER)
        except serial.SerialException:
            sys.stderr.write('Could not open serial port\n')
        else:
            self.textEdit.setText('Connect to {}\n'.format(write_port_name))
            self.set_daemon_thread(self.display_data)

    def send(self):
        message = self.lineEdit.displayText()
        try:
            address = int(re.findall("\d", message)[0])
            if self.checkBox_mistake.isChecked():
                self.station.write_frame(message.encode("utf-8", errors="ignore"), address, self.MISTAKE_FLAG)
            else:
                self.station.write_frame(message.encode("utf-8", errors="ignore"), address, self.MESSAGE_WITHOUT_MISTAKE)
        except IndexError:
            sys.stderr.write('What about destination address?\n')
        except (AttributeError, serial.SerialException):
            sys.stderr.write('You have problems with serial port\n')

    def set_daemon_thread(self, target):
        self.thread_read = threading.Thread(target=target)
        self.thread_read.daemon = True
        self.thread_read.start()

    def display_data(self):
        while self.station and self.station.read_channel.is_open:
            text = self.station.read_data()
            if text:
                print(''.join(text))

    def init_ring(self):
        if self.checkbox_active_station.isChecked():
            self.station.init_token_ring()

    def shutdown(self):
        try:
            self.station.shutdown()
        except serial.SerialException:
            sys.sdterr.write('You have problems with serial port\n')

    def disconnect(self):
        try:
            self.station.close_channels()
            self.station = None
        except serial.SerialException:
            sys.sdterr.write('You have problems with serial port\n')
        print('Disconnect')


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()


if __name__ == "__main__":
    main()



