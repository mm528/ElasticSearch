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

from PyQt5 import QtCore, QtGui, QtWidgets
import newuser
from PyQt5 import QtWidgets
import sqlite3




import argparse
from elasticsearch_dsl.query import Q



class UI (QMainWindow):
    def __init__(self):
        super(UI,self).__init__()

        uic.loadUi("C:/Users/motis/Desktop/groupPython/guiTest.ui",self)
        self.label = self.findChild(QLabel,"label")
        self.button = self.findChild(QPushButton, "pushButton")
        self.button2 = self.findChild(QPushButton, "pushButton_login")
        self.text = self.findChild(QTextEdit,"textEditLeft")
        self.text = self.findChild(QTextEdit,"textEditRight")

        button = QPushButton('Hey', self)
        button.setToolTip('This is an example button')
        button.move(100,70)
        


        button.clicked.connect(self.on_click)
        self.button.clicked.connect(self.clk)
        self.button2.clicked.connect(self.click2)
        self.show()

    @pyqtSlot()
    def on_click(self):
         self.label.setText('Connect with Elastic SEARCH! Print results') 
         print('Connect with Elastic SEARCH! Print results')
         print('Test git guys iam here e!')

    def click2(self):
          print('Here i need to find a connection between the words')
          Form = QtWidgets.QWidget()
          ui = login.Ui_Form()
          ui.setupUi(Form)
          Form.show()
          self.window = QtWidgets.QMainWindow()
          self.ui = login.Ui_Form()
          self.ui.setupUi(self.window)
          self.window.show()
          
          






    def clk(self):
          
          #retrieve data for id=2
          
          res = es.get(index="news", id='tLxuy3UBg-YlbYnR9IRP')
          j =  'Trying to find with the exact word                [all]   ' + json.dumps(res['_index'])
          k = json.dumps(res['_source']['text'])
          print (res)
          self.label.setText(j)
          self.text.setText(str(k))  
          for hit in res:
            print(hit)

          text = "London"
          index = "cities"
          try:
             client = Elasticsearch()
             s = Search(using=client, index="cities")
             if text is not None:
                    q = Q('multi_match', query=text, fields=['text'])
                    s = s.query(q)
                    s = s.highlight('text', fragment_size=10)
                    response = s.execute()
                    for r in s.scan(): # scan allows to retrieve all matches
                     print('ID= %s PATH=%s' % (r.meta.id, r.path))
                     for j, fragment in enumerate(r.meta.highlight.text):
                        print(' ->  TXT=%s' % fragment) 
           
                    q = Q('query_string',query='London')
                    s = s.query(q)
                    response = s.execute()
                    for r in s.scan(): # scan allows to retrieve all matches
                     print('ID= %s TXT=%s PATH=%s' % (r.meta.id, r.text[0:20], r.path))
                     print ('%d Documents' % response.hits.total.value) 
          except NotFoundError:
            print('Index %s does not exists' % index)   
         
           
           


          #s = Search(using=client, index="cities") \
           #.query("match", _source="London")
           

          #os.system('C:/Users/motis/Desktop/groupPython/SearchIndex.py')            
    




app = QApplication(sys.argv)
UIWindow = UI()
app.exec_()