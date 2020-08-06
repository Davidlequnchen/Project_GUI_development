'''
Developer : Chen Lequn, David

The back-end program for QT GUI interface

Serial communication between the GUI and Arduino

'''


from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QSize, QRect, QObject, pyqtSignal, QThread, pyqtSignal, pyqtSlot
import time
from PyQt5.QtWidgets import QApplication, QComboBox, QDialog, QMainWindow, QWidget, QLabel, QTextEdit, QListWidget, \
    QListView
from pyqtgraph.Qt import  QtCore
import pyqtgraph as pg
import pyqtgraph.exporters
import sys
from random import randint
from threading import Thread
from time import sleep

import sys, serial, serial.tools.list_ports, warnings




class Singnal_handler(QObject):
    # Self-defined QObject class，
    
    # Self-defined signals: define the signal objects parameters
    finished = pyqtSignal()
    intReady = pyqtSignal(str)

    @pyqtSlot()
    def __init__(self):
        super(Singnal_handler, self).__init__()
        self.working = True
        self.serial_communicate = None

    def work(self):
        while self.working:
            # receive the data as long as working is true
            line = self.serial_communicate.readline().decode('utf-8') # Read and return a list of lines from the stream
            # other python serial funcitons to read: read_until(expected=LF, size=None), read(size=1)
            # print(line)
            time.sleep(0.1)
            self.intReady.emit(line) # use the emit funciton to execute the signal
        self.finished.emit()




class Qt_controller():
    def __init__(self):
        # Load the UI file, all the buttons, widges from the front-end
        self.ui = uic.loadUi("GUI_motor_controller.ui")
        self.thread_data_receiver = None
        self.signal_handler = None
        self.serial_communicate = None
        #-------------------------------Initialize the plot area-----------------
        # voltagePlot is a pygraph.PlotWidget object
        self.ui.voltagePlot.setTitle("Voltage Plot",
                                    color='008080',
                                    size='12pt')  
        # set the labels
        self.ui.voltagePlot.setLabel("left","voltage [V]")
        self.ui.voltagePlot.setLabel("bottom","time [sec]")  
        
        # Set the Y-axis range
        self.ui.voltagePlot.setYRange(min=-10, # minimum Y value
                                    max=50)  # maximum Y value
        # Show the grid
        self.ui.voltagePlot.showGrid(x=True, y=True)
        #-----------------------------------------------------------------------
        # thread_cheching_port = Thread(target = self.port_detection,
        #                             args=())
        # thread_cheching_port.start()
        #----------------------------port detection - start-----------------------------------
        ports = [
            p.device
            for p in serial.tools.list_ports.comports()
            # if 'USB' in p.description
        ]
        if not ports: # if no ports detected, don't do anything
            self.ui.label_7.setText("No device connected!")
            self.ui.label_7.setStyleSheet('color: red')
            
        # if len(ports) > 1:
        else: # the Arduino device is connected
            # warnings.warn('Connected ...')
            self.ui.label_9.setText(ports[0]) # label 9 display the port name e.g.'COM3'
            self.serial_communicate = serial.Serial(ports[0],9600) # serial communication estabilished
            # self.serial_communicate.open() # Open port. The state of rts and dtr is applied.
            self.ui.label_7.setText("CONNECTED!")
            self.ui.label_7.setStyleSheet('color: green')
        #---------------------------------------------------------------------------------
        
        
        # buttons connection to the back-end functions
        self.ui.button_connect.clicked.connect(self.start_loop) # "connect button" is linked to the 'start_loop'
        self.ui.button_receive.clicked.connect(self.on_receive_button_clicked)
        self.ui.button_send.clicked.connect(self.on_send_button_clicked)
        self.ui.button_pause.clicked.connect(self.pause_loop)  # stop the loop on the stop button click
        self.ui.button_plot.clicked.connect(self.plot_button_clicked)
        self.ui.button_save.clicked.connect(self.save_button_clicked)



            
    def loop_finished(self):
        print('Looped Finished')
        # self.signal_handler.working = False


    def start_loop(self):
        '''
        This function initialze the connection between GUI and Arduino
        Multi-threading fuctionalities are initialzied
        '''

        # only connection is established will let the back-end receive data
        self.signal_handler = Singnal_handler()  # a new Singnal_handler to perform conduct sending signal
        self.signal_handler.serial_communicate = self.serial_communicate
        self.signal_handler.working = True
        self.thread_data_receiver = QThread()  # a new thread to run our background tasks 
        self.signal_handler.moveToThread(self.thread_data_receiver)  # move the Singnal_handler into the thread, do this first before connecting the signals
        self.thread_data_receiver.started.connect(self.signal_handler.work)
        # begin our Singnal_handler object's loop when the thread starts running
        self.signal_handler.intReady.connect(self.display_data) # connect the intReady signal to the "display_data" slot
        self.signal_handler.finished.connect(self.loop_finished)  # connect the finished signal to "loop_finished" slot
        self.signal_handler.finished.connect(self.thread_data_receiver.quit)  # tell the thread it's time to stop running(quit) if "finished" signal is invoked
        self.signal_handler.finished.connect(self.signal_handler.deleteLater)  # have Singnal_handler mark itself for deletion if "finished" signal is invoked
        self.thread_data_receiver.finished.connect(self.thread_data_receiver.deleteLater)  # have thread mark itself for deletion if "finished" signal is invoked
        # make sure those last two are connected to themselves or you will get random crashes
        self.thread_data_receiver.start() # start the thread for receiving data


    def pause_loop(self):
        self.ui.textEdit_2.setText('Stopped! Press CONNECT to reconnect ...')
        self.signal_handler = None

    def display_data(self, i):
        # this function receive the Arduino data and append it to display them in the Receive Console
        self.ui.textEdit_2.append("{}".format(i))
        
        
          
    def plot_button_clicked(self):
        # voltagePlot is a pygraph.PlotWidget object
        self.ui.voltagePlot.setTitle("Voltage Plot",
                                    color='008080',
                                    size='12pt')  
        # set the labels
        self.ui.voltagePlot.setLabel("left","voltage [V]")
        self.ui.voltagePlot.setLabel("bottom","time [sec]")  
        
        # Set the Y-axis range
        self.ui.voltagePlot.setYRange(min=-10, # minimum Y value
                                      max=50)  # maximum Y value
        # Show the grid
        self.ui.voltagePlot.showGrid(x=True, y=True)
        # change the plot area color to white
        self.ui.voltagePlot.setBackground('w')
        # make the display of PlotWidget in the central
        # self.setCentralWidget(self.ui.voltagePlot)
        
        # Real-time get the plotItem， use the setData funciton
        # Only re-plot this specific curve each time
        self.curve = self.ui.voltagePlot.getPlotItem().plot(
            pen=pg.mkPen('r', width=1)
        )
        
        
        self.i = 0
        self.x = [] # x轴的值
        self.y = [] # y轴的值
        
        # initalize the timer，refresh the data for every 1 seconds
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.updateData)
        self.timer.start(1000) # refresh every 1000 miliseconds = 1s
        
        
    def save_button_clicked(self):
        # create an exporter instance, as an argument give it
        # the item you wish to export
        plot = self.ui.voltagePlot.getPlotItem()
        exporter = pg.exporters.ImageExporter(plot)  
        # set export parameters if needed
        # exporter.parameters()['width'] = 100   # (note this also affects height parameter)
        # save to file
        exporter.export('fileName.png')
        exporter_csv = pg.exporters.CSVExporter(plot)
        exporter_csv.export('test.csv')


  
        
    def updateData(self):
        self.i += 1
        self.x.append(self.i)
        # 创建随机温度值
        self.y.append(randint(10,30))

        # plot data: x, y values
        self.curve.setData(self.x,self.y)  
          
          
    def on_receive_button_clicked(self):
        self.ui.textEdit_2.setText('Receiving Data ...')
      
      
    def on_send_button_clicked(self):
        # Send data from serial port:
        send_data = self.ui.textEdit_3.toPlainText() # data form the send text
        # print(send_data.encode())
        self.serial_communicate.write(send_data.encode()) # sned the data to Arduino
        
        self.completed = 0
        while self.completed < 100:
            self.completed += 0.001
            self.ui.progressBar.setValue(self.completed)

        





app = QApplication([])
qt_controller = Qt_controller()
qt_controller.ui.show()
app.exec_()


