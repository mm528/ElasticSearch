from pyspark.sql import SparkSession
spark = SparkSession.builder.appName('cluster').getOrCreate()

from pyspark.ml.clustering import KMeans

# Loads data.
dataset = spark.read.csv("C:/Users/motis/Desktop/groupPython/netflix_titles.csv",header=True,inferSchema=True)
dataset.head()
dataset.printSchema()

for row in dataset.head(10):
    print(row)
    print('\n')

dataset.describe().show()