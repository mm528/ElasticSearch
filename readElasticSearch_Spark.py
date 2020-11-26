from pyspark.sql.functions import col
from pyspark.ml.clustering import KMeans
from pyspark.sql import SparkSession
from elasticsearch import Elasticsearch
es = Elasticsearch("http://localhost:9200")
from pyspark.sql import SparkSession

spark = SparkSession.builder.master("local[*]").appName('cluster').config("spark.io.compression.codec",
"org.apache.spark.io.LZ4CompressionCodec").config("spark.sql.parquet.compression.codec", "uncompressed").getOrCreate()

conf = {"es.resource" : "index/type"}
rdd = SparkSession.newAPIHadoopRDD("org.elasticsearch.hadoop.mr.EsInputFormat",
                             "org.apache.hadoop.io.NullWritable",
                             "org.elasticsearch.hadoop.mr.LinkedMapWritable",
                             conf=conf)
