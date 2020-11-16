from elasticsearch import Elasticsearch
es = Elasticsearch("http://localhost:9200")
res = es.search(index="english", body={"from":0,"size":2,"query":{"match":{"sentence":"mike"}}})
print (res) 