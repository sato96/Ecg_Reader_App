import os
import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QFileDialog
from PyQt5.uic import loadUi
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from Code.DeviceConnection.ConnectionHandler import SocketConnection
from Code.AppConfiguration.ConfigurationHandler import ConfigurationHandler as Config
from PyQt5.QtWidgets import QMessageBox

import matplotlib.pyplot as plt
import matplotlib.animation as animation
from Code.SignalProcessing.Signal import Signal


class MyMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Carica l'interfaccia utente da ecg.ui
        ui_file_name = "GUI/ecg.ui"
        loadUi(ui_file_name, self)

        # Crea un oggetto Figure di Matplotlib
        self.fig = Figure()
        self.ax = self.fig.add_subplot(111)

        # Crea un oggetto FigureCanvas di Matplotlib collegato alla Figure
        self.canvas = FigureCanvas(self.fig)

        # Trova il layout in cui vuoi inserire il grafico e aggiungilo
        layout = QVBoxLayout(self.graphicsView)
        layout.addWidget(self.canvas)

        # Collega i pulsanti ai tuoi metodi
        self.pushButton_2.clicked.connect(self.onStart)
        self.pushButton.clicked.connect(self.onStop)
        self.save.clicked.connect(self.onSave)
        self.actionInfo.triggered.connect(self.onInfo)
        self.actionCarica_ECG.triggered.connect(self.onOpenFile)
        self.actionCartella_di_salvataggio.triggered.connect(self.onConfigDir)
        # Inizializza le variabili per l'animazione
        self.xdata, self.ydata = [], []
        self.line, = self.ax.plot([], [], lw=2)
        self.start = False
        self.configFile = 'AppConfiguration/config.json'
        #conf = Config.getConfiguration(self.configFile)
        #TODO metti try per intercettare gli errori di caricamento dei file
        self.host = Config.getConfiguration(self.configFile, 'ipDevice').split(':')[0] # The server's hostname or IP address
        self.port = int(Config.getConfiguration(self.configFile, 'ipDevice').split(':')[1])  # The port used by the server
        self.plotFreq = Config.getConfiguration(self.configFile, 'plotFrequence')
        self.saveDir = Config.getConfiguration(self.configFile, 'savePath')
        self.connector = SocketConnection(self.host, self.port, self.saveDir)

        # Crea un'unica istanza di animazione
        self.ani = animation.FuncAnimation(self.fig, self.update_plot,frames=None,init_func=self.init_plot,
                                           interval=self.plotFreq, repeat=True, save_count=100)
        self.ani.event_source.stop()

    def init_plot(self):
        self.ax.set_ylim(-10.1, 10.1)
        self.ax.set_autoscale_on(True)
        del self.xdata[:]
        del self.ydata[:]
        self.line.set_data([], [])
        return self.line,

    def update_plot(self, frame):
        if self.start:
            #time.sleep(0.01)
            s = []
            while len(s) == 0:
                s = self.connector.getBuffer()
            self.xdata = self.xdata + [x for x in range(len(self.xdata), len(self.xdata) + len(s))]
            self.ydata = self.ydata + s
            xmin, xmax = self.ax.get_xlim()
            if len(self.xdata) >= xmax:
                self.ax.set_xlim(len(self.xdata), len(self.xdata) + (5*len(s)))

            if max(s) >= self.ax.get_ylim()[1] or min(s) <= self.ax.get_ylim()[0]:
                self.ax.set_ylim(min(self.ydata) -(0.1*min(self.ydata)), max(self.ydata) + (0.1*max(self.ydata)))
            self.line.set_data(self.xdata, self.ydata)
        return self.line,

    def onStart(self):
        print('Acquisizione...')
        self.start = True
        self.connector.startRecording()
        self.ani.event_source.start()

    def onStop(self):
        print('Stop')
        self.connector.stopRecording()
        self.start = False
        self.ani.event_source.stop()

    def onSave(self):
        print('Salvataggio...')
        self.connector.stopRecording()
        sig = self.connector.getSignal()
        print(sig.getSignal())
        print(sig.file)
        txt = 'Ecg salvato in ' + sig.file
        self.popUpMsg(txt, 'Salvataggio', 'INFORMATION')

    def onInfo(self):
        infoText = 'Versione 1.0\nCredits ing. Tozzi Samuele\nContacts samtozzi.st@gmail.com'
        infoText = infoText + '\nParametri generali di sisterma:' + '\n' + str(Config.getConfiguration(self.configFile, None))
        self.popUpMsg(infoText, 'Crediti', type='INFORMATION')

    def onConfigDir(self):
        dir = str(QFileDialog.getExistingDirectory(self, "Selezione la cartella"))
        if dir != '':
            dir = dir + '/'
        Config.saveConfiguration('AppConfiguration/config.json', 'savePath', dir)
        self.realod()
    def onOpenFile(self):
        file = QFileDialog.getOpenFileName(caption='Scegli un ecg', directory='/', filter="Fogli elettronici (*.csv)")
        if file[0] != '':
            ecg = Signal(filePath=file[0])
            ecg.getSignal(unsafe=True)
            ecgFiltered = ecg.rmvMean()
            plt.plot(ecgFiltered)
            plt.show()
        else:
            self.popUpMsg('Non è stato selezionato alcun file',title='File vuoto', type='WARNING')

    def realod(self):
        self.host = Config.getConfiguration(self.configFile, 'ipDevice').split(':')[0] # The server's hostname or IP address
        self.port = int(Config.getConfiguration(self.configFile, 'ipDevice').split(':')[1])  # The port used by the server
        self.plotFreq = Config.getConfiguration(self.configFile, 'plotFrequence')
        self.saveDir = Config.getConfiguration(self.configFile, 'savePath')
        self.connector = SocketConnection(self.host, self.port, self.saveDir)
        self.ani.event_source.interval = self.plotFreq



    def popUpMsg(self, text, title = '', type = None):
        msg = QMessageBox()
        msg.setWindowTitle(title)
        msg.setText(text)
        if type == 'CRITICAL':
            msg.setIcon(QMessageBox.Critical)
        elif type == 'WARNING':
            msg.setIcon(QMessageBox.Warning)
        elif type == 'INFORMATION':
            msg.setIcon(QMessageBox.Information)
        elif type == 'QUESTION':
            msg.setIcon(QMessageBox.Question)
        x = msg.exec_()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MyMainWindow()
    main_window.show()
    sys.exit(app.exec_())