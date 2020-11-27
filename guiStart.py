#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
from logging import exception
import time
import importlib
import webbrowser
from tempfile import NamedTemporaryFile
import pandas as pd
import json
from pyspark.sql.functions import col
from pyspark.ml.clustering import KMeans
from pyspark.sql import SparkSession
from elasticsearch_dsl.query import Q
import argparse
import pandas as pd
from nltk.stem import LancasterStemmer
from nltk.stem import PorterStemmer
import nltk
import sqlite3
from PyQt5 import QtWidgets
import newuser
import requests
import login
from elasticsearch_dsl.connections import connections
from elasticsearch_dsl import Document, Date, Integer, Keyword, Text
from datetime import datetime
from elasticsearch_dsl import Search
import os
from collections import UserString
from elasticsearch.exceptions import NotFoundError
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QLabel, QMainWindow, QApplication, QTableView, QWidget, QPushButton, QTextEdit, QInputDialog, QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5 import uic
from PyQt5.QtCore import pyqtSlot, QAbstractTableModel
from elasticsearch import Elasticsearch
from elasticsearch_dsl import search
from pickle import STRING
import sys
import pandas as pd
from PyQt5.QtWidgets import QApplication, QTableView
from PyQt5.QtCore import QAbstractTableModel, Qt
from pyspark.sql import SparkSession
Qt = QtCore.Qt

valuesBox = []
getAnswer = True

globalPath = os.path.dirname(__file__) + "/"

es = Elasticsearch("http://localhost:9200")
spark = SparkSession.builder.master("local[*]").appName('cluster').config("spark.io.compression.codec",
                                                                          "org.apache.spark.io.LZ4CompressionCodec").config("spark.sql.parquet.compression.codec", "uncompressed").getOrCreate()
spark = SparkSession.builder.appName("NetflixCsv").getOrCreate()
df = spark.read.csv(path= globalPath + "netflix_titles.csv",
                    sep=",",
                    header=True,
                    quote='"',
                    schema="show_id INT , type string, title string, director string , cast string, country string, date_added DATE, release_year DATE, rating string, duration string, listed_in string , description string"
                    )
df.cache()
df.createOrReplaceTempView("netflix")



class UI (QMainWindow):

    def __init__(self):
        super(UI, self).__init__()

        """
        Here we are creating the GUI (Button, Text)

        """
        uic.loadUi(
            globalPath + "guiTest.ui", self)
        self.label = self.findChild(QLabel, "label")
        self.button2 = self.findChild(QPushButton, "pushButton_login")
        self.text = self.findChild(QTextEdit, "textEditLeft")
        self.textTopRight = self.findChild(QTextEdit, "textEditRight")
        self.button3 = self.findChild(QPushButton, "pushButton_getData")
        self.buttonExit = self.findChild(QPushButton, "pushButton_exit")
        self.sendFiles = self.findChild(QPushButton, "pushButton_SendFiles")
        self.table = self.findChild(QTableView, "tableView_results")
        self.button4 = self.findChild(QPushButton, "pushButton_elastic")
        self.textOut = self.findChild(QTextEdit, "textEdit_elastic")
        self.resultText = self.findChild(
            QTextEdit, "textEdit_Results_From_Elastic")

        # Here is for the seatch button (text and button)
        self.searchButton = self.findChild(
            QPushButton, "pushButton_search_Button")
        self.textSearch = self.findChild(QTextEdit, "textEdit_search")
        self.labelSearchResults = self.findChild(QLabel, "label_results")

        # Link shapes with functions

        self.searchButton.clicked.connect(self.clickSearch)
        self.buttonExit.clicked.connect(self.clickExit)
        self.sendFiles.clicked.connect(self.sendFilesDrag)
        self.button4.clicked.connect(self.click3)
        self.show()

    # Beggining of the elastic search (first apprach with button - probly needs to be deleted)

    @pyqtSlot()
    def on_click(self):
        self.label.setText('Connect with Elastic SEARCH! Print results')
        int('Connect with EΥlastic SEARCH! Print results')
       

    def clickExit(self):
        sys.exit()

    def sendFilesDrag(self):
        import browserFile
        import importlib
        importlib.reload(browserFile)


    def click2(self):  # create the WINDOW
        Form = QtWidgets.QWidget()
        ui = login.Ui_Form()
        ui.setupUi(Form)
        Form.show()
        self.window = QtWidgets.QMainWindow()
        self.ui = login.Ui_Form()
        self.ui.setupUi(self.window)
        self.window.show()

    def click3(self):  # search from the elastic search fully function
        try:
            client = Elasticsearch()
            res = es.search(index="movies", body={})
            sample = res['hits']['hits']
         

            s = Search(using=client, index="movies")
            #print(s)
            getText = self.textSearch.toPlainText()
            q = Q('match', title=getText)
            s = s.query(q)
            s = s.highlight('text', fragment_size=20)
            response = s.execute()
            allTogether = ''
            
            for hit in response.hits.hits:
                allTogether = allTogether + "\n" + hit._source.title + " ----> By" + hit._source.cast
                print('FROM FILE 1 >>>>')
            self.textOut.setText(allTogether)
            
            res = es.search(index="imdb", body={})
            sample = res['hits']['hits']
            

            s = Search(using=client, index="imdb")
            print('From FILE 2 ->>>>')
            getText = self.textSearch.toPlainText()
            q = Q('match', title=getText)
            s = s.query(q)
            s = s.highlight('text', fragment_size=20)
            response = s.execute()
            allTogether = ''
            for hit in response.hits.hits:
                allTogether = allTogether + "\n" + hit._source.title + "->>> By " + hit._source.country
                print('FROM FILE 2 >>>>')
            self.textOut.setText(allTogether)
        except NotFoundError:
            print('error not found')

         # Dialog MESSAGE   To ask the user if wants to stem the word
    def takeinputs(self, k):
        name, done1 = QtWidgets.QInputDialog.getText(
            self, 'Note', 'Are you sure you dont want to look with this?  \n' + '>>   '+k + '     YES   OR    NO    ')
        print(name)
        return name

    def sorryMessage(self):
        QMessageBox.about(
            self, "Error", "Iam affraid we are not having this word  \n into the Netflix data. Please try again")
    def sorryMessagenullfile(self):
            QMessageBox.about(
            self, "Error", "Please try again")

        # Focusing over here! we are collecting the data and do some processing

    def clickSearch(self):
        getoutLoop = True
        getAnswer = True
        porter = PorterStemmer()
        lancaster = LancasterStemmer()
        getText = self.textSearch.toPlainText()
        #getText = getText.lower()
        listWords2=getText.split(' ')
        #valuesBox.append(getText)
        print(len(valuesBox))
        if len(valuesBox) != 0:
            saveword = getText
            for i in range(len(valuesBox)):
                print(valuesBox)
                if len(valuesBox) == 0:
                    valuesBox.append(getText)
                    self.textTopRight.append(getText)
                

                else:
                    if valuesBox[i] == getText:
                        print('We have already search with this value')
                        getAnswer = False
                        try:
                           
                            f = pd.read_csv(r''+globalPath +getText + '.csv')
                        except IOError:
                            self.sorryMessagenullfile()

                        base_html = """
                    `   <!doctype html>
                        <html><head>
                        <meta http-equiv="Content-type" content="text/html; charset=utf-8">
                        <script type="text/javascript" src="https://ajax.googleapis.com/ajax/libs/jquery/2.2.2/jquery.min.js"></script>
                        <link rel="stylesheet" type="text/css" href="https://cdn.datatables.net/1.10.16/css/jquery.dataTables.css">
                        <script type="text/javascript" src="https://cdn.datatables.net/1.10.16/js/jquery.dataTables.js"></script>
                        </head><body>%s<script type="text/javascript">$(document).ready(function(){$('table').DataTable({
                            "pageLength": 50
                        });});</script>
                        </body></html>
                        """

                        def df_html(y):
                            """HTML table with pagination and other goodies"""
                            df_html = y.to_html()
                            return base_html % df_html

                        def df_window(x):
                            """Open dataframe in browser window using a temporary file"""
                            with NamedTemporaryFile(delete=False, suffix='.html', mode='w+', encoding='UTF8') as f:
                                f.write(df_html(x))
                            webbrowser.open(f.name)

                        michalis = pd.DataFrame(f)
                        df_window(michalis)

                        print(f)
                        print('SUCESS')
                        getoutLoop = False
                        break

            else:
                print('Not inside the list >>> ADD TO THE LIST')
                valuesBox.append(getText)
                self.textTopRight.append(getText)

        else:
            saveword = getText
            print('the list is empty')
            valuesBox.append(getText)
            self.textTopRight.append(getText)

        try:    
            
            # Here is where sql command comes in to resolve the problem of the search (ordered by type)
    
##############################################################################################################################
            if len(listWords2) >1:
                print('Leksis parapanw apo 1 character')
                dfQuery = spark.sql("Select * from netflix where title RLIKE  " + "'" + getText + "'or type RLIKE "+ "'"
                                                                                    + getText +"'or director RLIKE "+ "'" + getText +"' or cast RLIKE " + "'" +getText + "' or country RLIKE " 
                                                                                    + "'"+getText+"' or description RLIKE "+ "'" + getText +"' or duration RLIKE " + "'" +getText + "' or rating RLIKE " + "'"+getText+"'or listed_in RLIKE " + "'"+getText+"'" ) 
                print(dfQuery.collect())   

                if len(dfQuery.collect()) == 0:
                    self.sorryMessage()
                else:
                    df3 = pd.DataFrame(dfQuery.collect())
                    df3.to_csv(r''+globalPath+getText+'.csv')
                    base_html = """
                    <!doctype html>
                    <html><head>
                    <meta http-equiv="Content-type" content="text/html; charset=utf-8">
                    <script type="text/javascript" src="https://ajax.googleapis.com/ajax/libs/jquery/2.2.2/jquery.min.js"></script>
                    <link rel="stylesheet" type="text/css" href="https://cdn.datatables.net/1.10.16/css/jquery.dataTables.css">
                    <script type="text/javascript" src="https://cdn.datatables.net/1.10.16/js/jquery.dataTables.js"></script>
                    </head><body>%s<script type="text/javascript">$(document).ready(function(){$('table').DataTable({
                        "pageLength": 50
                    });});</script>
                    </body></html>
                    """

                    def df_html(y):
                        """HTML table with pagination and other goodies"""
                        df_html = y.to_html()
                        return base_html % df_html

                    def df_window(x):
                        """Open dataframe in browser window using a temporary file"""

                        with NamedTemporaryFile(delete=False, suffix='.html', mode='w+', encoding='UTF8') as f:
                            f.write(df_html(x))
                        webbrowser.open(f.name)

                    michalis2 = pd.DataFrame(df3)
                    df_window(michalis2)



###############################################################################################################################################
            else:
                print('Mono 1 leksi')
                dfQuery = spark.sql("Select * from netflix where title like" + "'% " + getText + "%' or  type like" + "'% " + getText + "%' or director like" + "'% " + getText + "%' or cast like" + "'% " + getText + "%' or country like" + "'%" + getText + "%'   or date_added like" +
                                    "'% " + getText + "%'  or release_year like" + "'% " + getText + "%'  or rating like" + "'% " + getText + "%'  or duration like" + "'% " + getText + "%'   or listed_in like" + "'% " + getText + "%' or description like" + "'% " + getText + "%' order by type")
                getText = porter.stem(getText)
                distData = spark.sql("Select * from netflix where title like" + "'% " + getText + "%' or  type like" + "'% " + getText + "%' or director like" + "'% " + getText + "%' or cast like" + "'% " + getText + "%' or country like" + "'%" + getText + "%'   or date_added like" +
                                    "'% " + getText + "%'  or release_year like" + "'% " + getText + "%'  or rating like" + "'% " + getText + "%'  or duration like" + "'% " + getText + "%'   or listed_in like" + "'% " + getText + "%' or description like" + "'% " + getText + "%' order by type")

                if (dfQuery.count() >= distData.count()): 
                    if (dfQuery.count() == 0):
                        self.sorryMessage()
                    else:
                        df3 = pd.DataFrame(dfQuery.collect())
                        df3.to_csv( r+''+globalPath+saveword+'.csv', index=False)
                        #j = dfQuery.select(col("*")).collect()
                        # self.resultText.append(str(j))
                        base_html = """

                        <!doctype html>
                        <html><head>
                        <meta http-equiv="Content-type" content="text/html; charset=utf-8">
                        <script type="text/javascript" src="https://ajax.googleapis.com/ajax/libs/jquery/2.2.2/jquery.min.js"></script>
                        <link rel="stylesheet" type="text/css" href="https://cdn.datatables.net/1.10.16/css/jquery.dataTables.css">
                        <script type="text/javascript" src="https://cdn.datatables.net/1.10.16/js/jquery.dataTables.js"></script>
                        </head><body>%s<script type="text/javascript">$(document).ready(function(){$('table').DataTable({
                            "pageLength": 50
                        });});</script>
                        </body></html>
                        """

                        def df_html(y):
                            """HTML table with pagination and other goodies"""
                            df_html = y.to_html()
                            return base_html % df_html

                        def df_window(x):
                            """Open dataframe in browser window using a temporary file"""

                            with NamedTemporaryFile(delete=False, suffix='.html', mode='w+', encoding='UTF8') as f:
                                f.write(df_html(x))
                            webbrowser.open(f.name)

                        michalis2 = pd.DataFrame(df3)
                        df_window(michalis2)
                else:
                    if getAnswer == True:
                        answer = self.takeinputs(getText)
                        if answer == 'YES':
                            print('Success')
                            df2 = pd.DataFrame(distData.collect())
                            df2.to_csv(
                                r''+globalPath+saveword+'.csv')

                            base_html = """
                            <!doctype html>
                            <html><head>
                            <meta http-equiv="Content-type" content="text/html; charset=utf-8">
                            <script type="text/javascript" src="https://ajax.googleapis.com/ajax/libs/jquery/2.2.2/jquery.min.js"></script>
                            <link rel="stylesheet" type="text/css" href="https://cdn.datatables.net/1.10.16/css/jquery.dataTables.css">
                            <script type="text/javascript" src="https://cdn.datatables.net/1.10.16/js/jquery.dataTables.js"></script>
                            </head><body>%s<script type="text/javascript">$(document).ready(function(){$('table').DataTable({
                                "pageLength": 50
                            });});</script>
                            </body></html>
                            """

                            def df_html(y):
                                """HTML table with pagination and other goodies"""
                                df_html = y.to_html()
                                return base_html % df_html

                            def df_window(x):
                                """Open dataframe in browser window using a temporary file"""
                                with NamedTemporaryFile(delete=False, suffix='.html', mode='w+', encoding='UTF8') as f:
                                    f.write(df_html(x))
                                webbrowser.open(f.name)

                            michalis = pd.DataFrame(df2)
                            df_window(michalis)
                        else:
                            print('Clicked NO')
                            df2 = pd.DataFrame(dfQuery.collect())
                            df2.to_csv(
                                r''+globalPath+saveword+'.csv', index=False)

                            base_html = """
                            <!doctype html>
                            <html><head>
                            <meta http-equiv="Content-type" content="text/html; charset=utf-8">
                            <script type="text/javascript" src="https://ajax.googleapis.com/ajax/libs/jquery/2.2.2/jquery.min.js"></script>
                            <link rel="stylesheet" type="text/css" href="https://cdn.datatables.net/1.10.16/css/jquery.dataTables.css">
                            <script type="text/javascript" src="https://cdn.datatables.net/1.10.16/js/jquery.dataTables.js"></script>
                            </head><body>%s<script type="text/javascript">$(document).ready(function(){$('table').DataTable({
                                "pageLength": 50
                            });});</script>
                            </body></html>
                            """

                            def df_html(y):
                                """HTML table with pagination and other goodies"""
                                df_html = y.to_html()
                                return base_html % df_html

                            def df_window(x):
                                """Open dataframe in browser window using a temporary file"""
                                with NamedTemporaryFile(delete=False, suffix='.html', mode='w+', encoding='UTF8') as f:
                                    f.write(df_html(x))
                                webbrowser.open(f.name)

                            michalis = pd.DataFrame(df2)
                            df_window(michalis)

                    else:
                        print('out of loop')

        except NotFoundError:
            print('Out of limit')


app = QApplication(sys.argv)
UIWindow = UI()

app.exec_()
app.setQuitOnLastWindowClosed(False)
