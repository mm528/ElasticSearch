from pyspark.sql import SparkSession
spark = SparkSession.builder.appName('cluster').getOrCreate()

from pyspark.ml.clustering import KMeans


spark = SparkSession.builder.appName("NetflixCsv").getOrCreate()
df = spark.read.csv(path = "C:/Users/motis/Desktop/groupPython/netflix_titles.csv",
    sep = ",",
    header = True,
    quote = '"',
    schema = "show_id INT , type string, title string, director string , cast string, country string, date_added DATE, release_year DATE, rating string, duration string, listed_in string , description string"
)

df.show(5)
df.printSchema()
# Loads data.
# dataset = spark.read.csv("C:/Users/motis/Desktop/groupPython/netflix_titles.csv",header=True,inferSchema=True)
# dataset.head()
# dataset.printSchema()

# for row in dataset.head(10):
#     print(row)
#     print('\n')

# dataset.describe().show()