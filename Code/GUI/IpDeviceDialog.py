from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi
from Code.AppConfiguration.ConfigurationHandler import ConfigurationHandler as Conf
from Code.GUI.PopUpMsg import PopUp


class IpDeviceDialog(QDialog):
    def __init__(self, configFile):
        super().__init__()
        self.configFile = configFile
        # Carica l'interfaccia
        ui_file_name = "GUI/IpDevice.ui"
        loadUi(ui_file_name, self)
        self.buttonBox.accepted.connect(self.handleOk)
        self.buttonBox.rejected.connect(self.handleCancel)
        self._param = 'ipDevice'

        defValue = Conf.getConfiguration(self.configFile, self._param)
        # Imposta un valore predefinito per la spin box
        self.lineEdit.setText(defValue)

    def handleOk(self):
        value = self.lineEdit.text()
        r = Conf.saveConfiguration(self.configFile, self._param, value)
        if r:
            self.close()
        else:
            PopUp.popUpMsg('Si è verificato un errore nel salvataggio', 'Errore!', 'CRITICAL')
            print('errore')

    def handleCancel(self):
        self.close()
