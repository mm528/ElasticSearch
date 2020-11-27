#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QListWidget, QListWidgetItem, QPushButton, QInputDialog, QLineEdit
from PyQt5.QtCore import Qt, QUrl
import IndexFiles
import time
import os
import sys
globalText = ''
x=''
######################################## DRAG AND DROP UPLOAD FILE #######################################################
######################################## FULLY FUNCTION BUT WE PREFER THE ORIGINAL FILE ###################################3
class ListBoxWidget(QListWidget):

    def __init__(self, parent=None):
        
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.resize(300, 300)

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
                    
                    self.addItems(links)
                else:
                    links.append(str(url.toString()))
                    
                    self.addItems(links)
        else:
            event.ignore()
            print('error!')


class AppDemo(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(500, 300)

        self.listbox_view = ListBoxWidget(self)

        self.btn = QPushButton('Get Value', self)
        self.btn.setGeometry(300, 200, 200, 50)
        self.btn.clicked.connect(lambda: print(self.getSelectedItem()))
        self.btn.clicked.connect(self.upload)

    def upload(self):
        text, okPressed = QInputDialog.getText(
            self, "Get text", "Please provide your index Name", QLineEdit.Normal, "")
        if okPressed and text != '':
            text2, okPressed = QInputDialog.getText(
                self, "Get text", "Please provide your Type Name", QLineEdit.Normal, "")
            if okPressed and text != '':
                #print(text, text2, self.getSelectedItem())
                import sys
                f = self.getSelectedItem();
                #####################################################################################################################3
                print(f)
                print(globalText)
                import csv
                import json
                import re
                file = open(""+str(f), "r", encoding='UTF8') #Edw to diavazi me UTF8 (SIMANTIKO)
                dict_reader = csv.DictReader(file)
                dict_from_csv = list(dict_reader)
                json_from_csv = json.dumps(dict_from_csv)        
                with open(""+str(f),'rt',encoding='UTF8')as f:
                    data = csv.reader(f,delimiter = '\t')
                    for row in data:
                        print(row)
                        delchars = ''.join(c for c in map(chr, range(256)) if not c.isalnum())
                        re.sub(r'\delchars+', '', 'skjbfaesjfbcs')
                        letters_only = re.sub("½", "", row[0])
                        letters_only = re.sub("ï", "", letters_only)
                        letters_only = re.sub("#", "", letters_only)
                        letters_only = re.sub("NaN", "", letters_only) ###>>>> AFAIROUME OLA TA PERITTA P DEN THELOUME STO JSON!!
                        #print(letters_only)
                        with open(text + ".json", "w") as outfile:
                            outfile.write(json_from_csv)

                        
               
              
            
               ####################################################################################################################
                
                print(sys.argv) 
                input("Enter")    
                try:
                    # time.sleep(10)
                    # script_descriptor = open("elasticsearch_loader.py")
                    # a_script = script_descriptor.read()
                    # jsonName = text +".json"
                    # sys.argv = ["elasticsearch_loader.py", "--index", "michalis", "--type", "michalis" , "json" , "michalis.json"]
                    # exec(a_script)
                    import runPython
                    
                except TimeoutError:
                   
                    import runPython
                   



                ###########################################################################################################3



















               ###########################################################################################################################
                # print(sys.argv)
                # time.sleep(3)
                # script_descriptor = open("elasticsearch_loader.py")
                # a_script = script_descriptor.read()
                # sys.argv = ["elasticsearch_loader.py", "--index", text, "--type", text2, "json" , "michalis.json"]
                # time.sleep(2)
                # exec(a_script)
                

            # IndexFiles.main(self.getSelectedItem(), text)
            #  print('here')
            #  import sys
            #  sys.argv = ["elasticsearch_loader.py", "--index", "testsdv" , "--type", "testdsvs" , "json" , "michalis.json"]
            #  print(sys.argv)

            #  import time

            #  script_descriptor = open("elasticsearch_loader.py" + " --index", "tes" , " --type", "tes" , "json" , "michalis.json")

            #  a_script = script_descriptor.read()
            #  sys.argv = ["elasticsearch_loader.py", "--index", "tes" , "--type", "tes" , "json" , "michalis.json"]

            #  exec(script_descriptor)
            #import runPython

    def getSelectedItem(self):
        item = QListWidgetItem(self.listbox_view.currentItem())
        globalText = item.text()
        return str(item.text())


def main():
    demo = AppDemo()
    demo.show()
