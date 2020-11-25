from __future__ import print_function
import time
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
answer = 'false'
es = Elasticsearch("http://localhost:9200")
spark = SparkSession.builder.master("local[*]").appName('cluster').config("spark.io.compression.codec",
                                                                          "org.apache.spark.io.LZ4CompressionCodec").config("spark.sql.parquet.compression.codec", "uncompressed").getOrCreate()
spark = SparkSession.builder.appName("NetflixCsv").getOrCreate()
df = spark.read.csv(path="C:/Users/motis/Desktop/groupPython/netflix_titles.csv",
                    sep=",",
                    header=True,
                    quote='"',
                    schema="show_id INT , type string, title string, director string , cast string, country string, date_added DATE, release_year DATE, rating string, duration string, listed_in string , description string"
                    )
df.cache()
df.createOrReplaceTempView("netflix")
dfTEST = pd.read_csv('netflix_titles.csv')


class UI (QMainWindow):

    def __init__(self):
        super(UI, self).__init__()

        """
        Here we are creating the GUI (Button, Text)

        """
        uic.loadUi("C:/Users/motis/Desktop/groupPython/guiTest.ui", self)
        self.label = self.findChild(QLabel, "label")
        self.button2 = self.findChild(QPushButton, "pushButton_login")
        self.text = self.findChild(QTextEdit, "textEditLeft")
        self.textTopRight = self.findChild(QTextEdit, "textEditRight")
        self.button3 = self.findChild(QPushButton, "pushButton_getData")
        self.buttonExit = self.findChild(QPushButton, "pushButton_exit")
        self.sendFiles = self.findChild(QPushButton, "pushButton_SendFiles")
        self.table = self.findChild(QTableView, "tableView_results")
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

        self.show()

    # Beggining of the elastic search (first apprach with button - probly needs to be deleted)

    @pyqtSlot()
    def on_click(self):
        self.label.setText('Connect with Elastic SEARCH! Print results')
        print('Connect with Elastic SEARCH! Print results')
        print('Test git guys iam here e!')

    def clickExit(self):
        sys.exit()

    def sendFilesDrag(self):
        import importFiles_Drag_And_Drop
        importFiles_Drag_And_Drop.main()

    def click2(self):  # create the WINDOW

        Form = QtWidgets.QWidget()
        ui = login.Ui_Form()
        ui.setupUi(Form)
        Form.show()
        self.window = QtWidgets.QMainWindow()
        self.ui = login.Ui_Form()
        self.ui.setupUi(self.window)
        self.window.show()

    def click3(self):  # search from the elastic search
        try:
            client = Elasticsearch()
            res = es.search(index="movies_netflix", body={})
            sample = res['hits']['hits']
            for hit in sample:
                print(hit)

            s = Search(using=client, index="movies_netflix")
            print(s)
            q = Q('match_all')
            s = s.query(q)
            s = s.highlight('text', fragment_size=20)
            response = s.execute()
            allTogether = ''
            for hit in response.hits.hits:
                allTogether = allTogether + "\n" + hit._source.director
                print(hit._source.director)
            self.labelSearchResults.setText(allTogether)
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

        # Focusing over here! we are collecting the data and do some processing

    def clickSearch(self):
        porter = PorterStemmer()
        lancaster = LancasterStemmer()

        getText = self.textSearch.toPlainText()

        print(getText)
        self.textTopRight.append(getText)

        try:

            # Here is where sql command comes in to resolve the problem of the search (ordered by type)

            dfQuery = spark.sql("Select * from netflix where title like" + "'% " + getText + "%' or  type like" + "'% " + getText + "%' or director like" + "'% " + getText + "%' or cast like" + "'% " + getText + "%' or country like" + "'%" + getText + "%'   or date_added like" +
                                "'% " + getText + "%'  or release_year like" + "'% " + getText + "%'  or rating like" + "'% " + getText + "%'  or duration like" + "'% " + getText + "%'   or listed_in like" + "'% " + getText + "%' or description like" + "'% " + getText + "%' order by type")
            getText = porter.stem(getText)
            distData = spark.sql("Select * from netflix where title like" + "'% " + getText + "%' or  type like" + "'% " + getText + "%' or director like" + "'% " + getText + "%' or cast like" + "'% " + getText + "%' or country like" + "'%" + getText + "%'   or date_added like" +
                                 "'% " + getText + "%'  or release_year like" + "'% " + getText + "%'  or rating like" + "'% " + getText + "%'  or duration like" + "'% " + getText + "%'   or listed_in like" + "'% " + getText + "%' or description like" + "'% " + getText + "%' order by type")

            print(getText)
            if (dfQuery.count() >= distData.count()):
                if (dfQuery.count() == 0):
                    self.sorryMessage()
                else:
                    df3 = pd.DataFrame(dfQuery.collect())
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
                # check with stemming,. better search!
                # We can cerate a list over here to have the data in a nice formS
                # k = dfQuery.select(col("title")).collect()
                # self.resultText.append(str(k))

                answer = self.takeinputs(getText)
                if answer == 'YES':
                    print('Success')
                    df2 = pd.DataFrame(distData.collect())
                    1  # print(df2)
                    # thelw na fkalw to window!
                    #import testPanda
                    # testPanda.createTable()
                    #k = distData.select(col("*")).collect()
                    # self.resultText.append(str(k))

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
                    df3 = pd.DataFrame(dfQuery.collect())
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

        except NotFoundError:
            print('Out of limit')

            # s = Search(using=client, index="cities") \
            # .query("match", _source="London")

        # os.system('C:/Users/motis/Desktop/groupPython/SearchIndex.py')


app = QApplication(sys.argv)
UIWindow = UI()
app.exec_()
app.setQuitOnLastWindowClosed(False)
