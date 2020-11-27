
import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QFileDialog,
                             QTextEdit, QPushButton, QLabel, QVBoxLayout, QInputDialog, QLineEdit,QMessageBox)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QCoreApplication, QDir
from PyQt5 import QtCore
indexName=''
typeIndexname=''
path=''

class DialogApp(QWidget):
    

    globalName = ''
    def setIndex(self,ndname):
        indexName = ndname
    def settype(self,typename):
        typeIndexname = typename
    def setpath(self,pathname):
        path = pathname

    
    def getNameIndex(self):
        return typeIndexname
    def getPathname(self):
        return path
    def getIndexName(self):
        return indexName
    
    
       

    

    def __init__(self):
        
        super().__init__()
        self.resize(1200, 800)

        self.button1 = QPushButton('Have a pic look on your file')
        self.button1.clicked.connect(self.get_file)

        self.button2 = QPushButton('Upload and convert to Json')
        self.button2.clicked.connect(self.get_text_file)

        self.labelImage = QLabel()
        self.textEditor = QLineEdit()

        layout = QVBoxLayout()
        layout.addWidget(self.button1)
        layout.addWidget(self.labelImage)
        layout.addWidget(self.button2)
        layout.addWidget(self.textEditor)
        self.setLayout(layout)
#############################################################################################################
    def get_file(self):
        dialog2 = QFileDialog()
        dialog2.setFileMode(QFileDialog.AnyFile)
        dialog2.setFilter(QDir.Files)
        if dialog2.exec_():
            file_name = dialog2.selectedFiles()
            try:
                if file_name[0].endswith('.csv'):
                    with open(file_name[0], 'r') as f:
                        data= f.read()
            
                        self.textEditor.setText(data[1:]) ## >>>> pic of the file
            except FileNotFoundError:
                print('Cannt read')
                        
            
################################################################################################################

    def get_text_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, 'Open File', r"<Default dir>", "")
        globalName = file_name
        print(file_name)
        text, okPressed = QInputDialog.getText(
            self, "Get text", "Please provide your index Name", QLineEdit.Normal, "")
        if okPressed and text != '':
            text2, okPressed = QInputDialog.getText(
                self, "Get text", "Please provide your Type Name", QLineEdit.Normal, "")
            if okPressed and text != '':
                print(text+ " " + text2 + " >>>" + globalName)
                #print(text, text2, self.getSelectedItem())
                self.setIndex(text)
                self.settype(text2)
                import sys


                #####################################################################################################################3
                
                import csv
                import json
                import re
                filepassword = open("password.txt","w")
                file = open(""+str(globalName), "r", encoding='UTF8') #Edw to diavazi me UTF8 (SIMANTIKO)
                dict_reader = csv.DictReader(file)
                dict_from_csv = list(dict_reader)
                json_from_csv = json.dumps(dict_from_csv)        
                with open(""+str(globalName),'rt',encoding='UTF8')as f:
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
                    jsonName = text+".json" 
                    filepassword.write(text + " "+ text2 + " "+ jsonName)
                    filepassword.close
                 ####################################################################################################################
                
                print(sys.argv)     
                try:
                    msg = QMessageBox()
                    msg.setWindowTitle("Will exit the system")
                    import browserFile
                    import runPython
                   
                except TimeoutError:
                    print('run out')
                    import runPython                


demo = DialogApp()
demo.show()


