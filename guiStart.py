from __future__ import print_function
from collections import UserString
from elasticsearch.exceptions import NotFoundError
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QLabel,QMainWindow,QApplication, QWidget, QPushButton,QTextEdit
from PyQt5.QtGui import QIcon
from PyQt5 import uic
from PyQt5.QtCore import pyqtSlot
from elasticsearch import Elasticsearch
from elasticsearch_dsl import search
es = Elasticsearch("http://localhost:9200")
import json 
import os
from elasticsearch_dsl import Search
from datetime import datetime
from elasticsearch_dsl import Document, Date, Integer, Keyword, Text
from elasticsearch_dsl.connections import connections
import login
import requests
from PyQt5 import QtCore, QtGui, QtWidgets
import newuser
from PyQt5 import QtWidgets
import sqlite3
import nltk
from nltk.stem import PorterStemmer
from nltk.stem import LancasterStemmer
import argparse
from elasticsearch_dsl.query import Q



class UI (QMainWindow):
    #nltk.download()
   
    def __init__(self):
        super(UI,self).__init__()

        uic.loadUi("C:/Users/motis/Desktop/groupPython/guiTest.ui",self)
        self.label = self.findChild(QLabel,"label")
        self.button2 = self.findChild(QPushButton, "pushButton_login")
        self.text = self.findChild(QTextEdit,"textEditLeft")
        self.textTopRight = self.findChild(QTextEdit,"textEditRight")
        self.button3 = self.findChild(QPushButton, "pushButton_getData") 
        self.buttonExit = self.findChild(QPushButton, "pushButton_exit")
        self.sendFiles = self.findChild(QPushButton, "pushButton_SendFiles")

        #Here is for the seatch button (text and button)
        self.searchButton = self.findChild(QPushButton, "pushButton_search_Button") 
        self.textSearch = self.findChild(QTextEdit,"textEdit_search")
        self.labelSearchResults = self.findChild(QLabel, "label_results")

        button = QPushButton('Hey', self)
        button.setToolTip('This is an example button')
        button.move(100,70)
        


        button.clicked.connect(self.on_click)
        self.button2.clicked.connect(self.click2)
        self.button3.clicked.connect(self.click3)
        self.searchButton.clicked.connect(self.clickSearch)
        self.buttonExit.clicked.connect(self.clickExit)
        self.sendFiles.clicked.connect(self.sendFilesDrag)
        

        self.show()

    @pyqtSlot()
    def on_click(self):
         self.label.setText('Connect with Elastic SEARCH! Print results') 
         print('Connect with Elastic SEARCH! Print results')
         print('Test git guys iam here e!')

    def clickExit(self):
        sys.exit()

    def sendFilesDrag(self): 
        
        import  importFiles_Drag_And_Drop 
        importFiles_Drag_And_Drop.main()

    def click2(self):
          
          Form = QtWidgets.QWidget()
          ui = login.Ui_Form()
          ui.setupUi(Form)
          Form.show()
          self.window = QtWidgets.QMainWindow()
          self.ui = login.Ui_Form()
          self.ui.setupUi(self.window)
          self.window.show()
          
    def click3(self):
          text = "England"
          index = "cities"
          print ('iam here now')
          try:
             client = Elasticsearch()
             s = Search(using=client, index="news")
             if text is not None:
                    q = Q('multi_match', query=text, fields=['text']) 
                    s = s.query(q)
                    s = s.highlight('text', fragment_size=10)
                    response = s.execute()
                    
                 
                    for r in s.scan(): # scan allows to retrieve all matches
                     print('ID= %s PATH=%s' % (r.meta.id, r.path))
                     for j, fragment in enumerate(r.meta.highlight.text):
                        print(' ->  TXT=%s' % fragment) 

                    q = Q('query_string',query='England')
                    s = s.query(q)
                    response = s.execute()
                    for r in s.scan(): # scan allows to retrieve all matches
                     print('ID= %s TXT=%s PATH=%s' % (r.meta.id, r.text[0:20], r.path))
                    for hit in response.hits.hits:
                          self.textTopRight.append("From the document -> " + hit._source.path[25:50])
                          #self.text.append(hit._source.text) #here you can see the right TEXT ! ! <hits.hits.text>
                          
                      
                    #getasString =  response
                    print ('%d Documents' % response.hits.total.value) 
                   # self.text.append(getasString) s
          except NotFoundError:
            print('Index %s does not exists' % index)
           

    def clickSearch(self):
          porter = PorterStemmer()
          lancaster=LancasterStemmer()
          self.textTopRight.setText("")
          getText = self.textSearch.toPlainText()
          getText = porter.stem(getText)
          print(getText)
          try:
                client = Elasticsearch()
                s = Search(using=client, index="news")
                if getText is not None:
                    q = Q('multi_match', query=getText, fields=['text']) 
                    s = s.query(q)
                    s = s.highlight('text', fragment_size=10)
                    response = s.execute()
                    
                 
                    for r in s.scan(): # scan allows to retrieve all matches
                     print('ID= %s PATH=%s' % (r.meta.id, r.path))
                     for j, fragment in enumerate(r.meta.highlight.text):
                        print(' ->  TXT=%s' % fragment) 

                    q = Q('query_string',query='England')
                    s = s.query(q)
                    response = s.execute()
                    for r in s.scan(): # scan allows to retrieve all matches
                     print('ID= %s TXT=%s PATH=%s' % (r.meta.id, r.text[0:20], r.path))
                     if response.hits.total.value >0:
                         allTogether =''
                         for hit in response.hits.hits:

                              self.textTopRight.append("From the document -> " + hit._source.path[25:50])
                              allTogether = allTogether + "  \n  " + hit._source.text[60:90] + "\n "+ hit._source.path[25:50] +"\n"
                        
            
                          #self.text.append(hit._source.text) #here you can see the right TEXT ! ! <hits.hits.text>
                         self.labelSearchResults.setText(allTogether + str(response.hits.total.value))
                     elif response.hits.total.value == 0:
                            print('not found')
                      
                    #getasString =  response
                    #print ('%d Documents' % response.hits.total.value) 
                   # self.text.append(getasString) s
          except NotFoundError:
            print('Index %s does not exists' % index)


          #s = Search(using=client, index="cities") \
           #.query("match", _source="London")
           

          #os.system('C:/Users/motis/Desktop/groupPython/SearchIndex.py')            
    




app = QApplication(sys.argv)
UIWindow = UI()
app.exec_()