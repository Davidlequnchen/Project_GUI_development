__author__ = 'Mehmet Cagri Aksoy - github.com/mcagriaksoy'

import sys, serial, serial.tools.list_ports, warnings
from PyQt5.QtCore import QSize, QRect, QObject, pyqtSignal, QThread, pyqtSignal, pyqtSlot
import time
from PyQt5.QtWidgets import QApplication, QComboBox, QDialog, QMainWindow, QWidget, QLabel, QTextEdit, QListWidget, \
    QListView
from PyQt5.uic import loadUi

#port detection - start
ports = [
    p.device
    for p in serial.tools.list_ports.comports()
    # if 'USB' in p.description
]

if not ports:
    raise IOError("There is no serial connected device!")

if len(ports) > 1:
    warnings.warn('Connected ...')

ser = serial.Serial(ports[0],9600)
#port tespit etme - son


# class Foo(QThread):

#    def connect(self):
#        connect(pushButton_2, SIGNAL("clicked()"), on_pushButton_2_clicked)

# MULTI-THREADING

class Worker(QObject):
    finished = pyqtSignal()
    intReady = pyqtSignal(str)

    @pyqtSlot()
    def __init__(self):
        super(Worker, self).__init__()
        self.working = True

    def work(self):
        while self.working:
            line = ser.readline().decode('utf-8')
            print(line)
            time.sleep(0.1)
            self.intReady.emit(line)
            # if line != '':
            # self.textEdit_3.append(line)

        self.finished.emit()

class qt(QMainWindow):

    def __init__(self):

        QMainWindow.__init__(self)
        loadUi('qt.ui', self)
        # self.comboBox_0.activated.connect(self.load_value0)
        # self.comboBox_1.activated.connect(self.load_value1)
        self.thread = None
        self.worker = None
        self.pushButton.clicked.connect(self.start_loop)
        # print(self.comboBox_1.itemText(index1))
        self.label_11.setText(ports[0])

    def loop_finished(self):
        print('Looped Finished')

    def start_loop(self):

        self.worker = Worker()  # a new worker to perform those tasks
        self.thread = QThread()  # a new thread to run our background tasks in
        self.worker.moveToThread(
            self.thread)  # move the worker into the thread, do this first before connecting the signals

        self.thread.started.connect(self.worker.work)
        # begin our worker object's loop when the thread starts running

        self.worker.intReady.connect(self.onIntReady)

        self.pushButton_2.clicked.connect(self.stop_loop)  # stop the loop on the stop button click

        self.worker.finished.connect(self.loop_finished)  # do something in the gui when the worker loop ends
        self.worker.finished.connect(self.thread.quit)  # tell the thread it's time to stop running
        self.worker.finished.connect(self.worker.deleteLater)  # have worker mark itself for deletion
        self.thread.finished.connect(self.thread.deleteLater)  # have thread mark itself for deletion
        # make sure those last two are connected to themselves or you will get random crashes
        self.thread.start()

    def stop_loop(self):
        self.worker.working = False

    def onIntReady(self, i):
        self.textEdit_3.append("{}".format(i))
        print(i)

    # def load_value0(self, index0):
    #     portadi
    #   self.a2 = self.comboBox_0.itemText(index0)

    #  print(self.comboBox_0.itemText(index0))
    # self.x = 2

    # def load_value1(self, index1):
    # baudrate
    # b2 = self.comboBox_1.itemText(index1)
    # print(self.comboBox_1.itemText(index1))
    # self.x = 1

    # saving settings
    def on_pushButton_4_clicked(self):
        if self.x != 0:
            self.textEdit.setText('Settings Saved!')
        else:
            # print('error')
            self.textEdit.setText('Please enter Port and Speed!')

    # TXT PRINT ------ SAVE
    def on_pushButton_5_clicked(self):
        with open('Sonuc.txt', 'w') as f:
            my_text = self.textEdit_3.toPlainText()
            f.write(my_text)

    def on_pushButton_2_clicked(self):
        self.textEdit.setText('Stopped! Press CONNECT to reconnect ...')

    def on_pushButton_clicked(self):

        self.completed = 0
        while self.completed < 100:
            self.completed += 0.001
            self.progressBar.setValue(self.completed)
        self.textEdit.setText('Receiving Data ...')

        # self.label_5.setText('OK!')

        self.label_5.setText("CONNECTED!")
        self.label_5.setStyleSheet('color: green')
        x = 1
        self.textEdit_3.setText(":")

    def on_pushButton_3_clicked(self):
        # Send data from serial port:
        mytext = self.textEdit_2.toPlainText()
        print(mytext.encode())
        ser.write(mytext.encode())

def run():
    app = QApplication(sys.argv)
    widget = qt()
    widget.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    run()