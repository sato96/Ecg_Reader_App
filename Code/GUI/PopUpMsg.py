from PyQt5.QtWidgets import QMessageBox

class PopUp:
    @staticmethod
    def popUpMsg(text, title = '', type = None):
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