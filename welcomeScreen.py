from PyQt5 import QtWidgets, uic
import sys
import time

class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('welcome.ui', self)
        self.show()
        

window = Ui()
window.close
