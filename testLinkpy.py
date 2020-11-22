
from elasticsearch import Elasticsearch
es2 = Elasticsearch("http://localhost:9200")

print ('hkosdcs')
#{u'_type': u'places', u'_source': {u'city': u'London', u'country': u'England'}, u'_index': u'cities', u'_version': 13, u'found': True, u'_id': u'2'}

print ('_source')
#{u'city': u'London', u'country': u'England'}