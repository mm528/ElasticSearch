import sys
import pandas as pd
from PyQt5.QtWidgets import QApplication, QTableView
from PyQt5.QtCore import QAbstractTableModel, Qt
from pyspark.sql import SparkSession
from pandasgui import show
from PySide2 import QtCore, QtWidgets
from tempfile import NamedTemporaryFile
import webbrowser
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

df = pd.read_csv('netflix_titles.csv')


class pandasModel(QAbstractTableModel):
    def __init__(self, data):
        QAbstractTableModel.__init__(self)
        self._data = data

    def rowCount(self, parent=None):
        return self._data.shape[0]

    def columnCount(self, parnet=None):
        return self._data.shape[1]

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            if role == Qt.DisplayRole:
                return str(self._data.iloc[index.row(), index.column()])
        return None

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._data.columns[col]
        return None

def df_window(df):
    with NamedTemporaryFile(delete=False, suffix='.html') as f:
        df.to_html(f)
        webbrowser.open(f.name)

        
df_window(df)

# def createTable():
#     model = pandasModel(df)
#     view = QTableView()
#     view.setModel(model)
#     view.resize(800, 600)
#     view.show()
#  #
    

