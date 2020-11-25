from pyspark.sql import SparkSession
spark = SparkSession.builder.appName('cluster').getOrCreate()

from pyspark.ml.clustering import KMeans
import pandas as pd
from pandasgui import show



from tempfile import NamedTemporaryFile
import webbrowser
import pandas as pd
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

def df_html(df):
    """HTML table with pagination and other goodies"""
    df_html = df.to_html()
    return base_html % df_html

def df_window(df):
    """Open dataframe in browser window using a temporary file"""
    with NamedTemporaryFile(delete=False, suffix='.html',mode='w+') as f:
        f.write(df_html(df))
    webbrowser.open(f.name)
    
spark = SparkSession.builder.appName("NetflixCsv").getOrCreate()
p = spark.read.csv(path = "C:/Users/motis/Desktop/groupPython/netflix_titles.csv",
    sep = ",",
    header = True,
    quote = '"',
    schema = "show_id INT , type string, title string, director string , cast string, country string, date_added DATE, release_year DATE, rating string, duration string, listed_in string , description string"
)

df = p.toPandas
print(df.head)
#df_window(df)















#df.show(5)
#df.printSchema()
#df.show()
# df2 = pd.DataFrame(df.show())
# show(df2)

# Loads data.
# dataset = spark.read.csv("C:/Users/motis/Desktop/groupPython/netflix_titles.csv",header=True,inferSchema=True)
# dataset.head()
# dataset.printSchema()

# for row in dataset.head(10):
#     print(row)
#     print('\n')

# dataset.describe().show()