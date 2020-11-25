import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QListWidget, QListWidgetItem, QPushButton, QInputDialog, QLineEdit
from PyQt5.QtCore import Qt, QUrl
import IndexFiles
import time
import os
globalText = ''


class ListBoxWidget(QListWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.resize(600, 600)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls:
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls():
            event.setDropAction(Qt.CopyAction)
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            event.setDropAction(Qt.CopyAction)
            event.accept()

            links = []
            for url in event.mimeData().urls():

                if url.isLocalFile():
                    links.append(str(url.toLocalFile()))
                else:
                    links.append(str(url.toString()))
            self.addItems(links)
        else:
            event.ignore()


class AppDemo(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(1200, 600)

        self.listbox_view = ListBoxWidget(self)

        self.btn = QPushButton('Get Value', self)
        self.btn.setGeometry(850, 400, 200, 50)
        self.btn.clicked.connect(lambda: print(self.getSelectedItem()))
        self.btn.clicked.connect(self.upload)

    def upload(self):
        text, okPressed = QInputDialog.getText(
            self, "Get text", "Please provide your index Name", QLineEdit.Normal, "")
        if okPressed and text != '':
             # IndexFiles.main(self.getSelectedItem(), text)
             print('here')
             import sys
             sys.argv = ["elasticsearch_loader.py", "--index", "testsdv" , "--type", "testdsvs" , "json" , "michalis.json"]
             print(sys.argv)

             import time
             
             script_descriptor = open("elasticsearch_loader.py")
             
             a_script = script_descriptor.read()
             sys.argv = ["elasticsearch_loader.py", "--index", "tes" , "--type", "tes" , "json" , "michalis.json"]
         
             exec(a_script)


    def getSelectedItem(self):
        item = QListWidgetItem(self.listbox_view.currentItem())
        globalText = item.text()
        return str(item.text())
 
    
def main(): 
        demo = AppDemo()
        demo.show()

       
