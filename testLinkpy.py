
from elasticsearch import Elasticsearch
es2 = Elasticsearch("http://localhost:9200")

print ('hkosdcs')
#{u'_type': u'places', u'_source': {u'city': u'London', u'country': u'England'}, u'_index': u'cities', u'_version': 13, u'found': True, u'_id': u'2'}

print ('_source')
#{u'city': u'London', u'country': u'England'}

#  def upload(self):
#         text, okPressed = QInputDialog.getText(
#             self, "Get text", "Please provide your index Name", QLineEdit.Normal, "")
#         if okPressed and text != '':
#              text2, okPressed = QInputDialog.getText(
#              self, "Get text", "Please provide your Type Name", QLineEdit.Normal, "")
#              if okPressed and text != '':
#                  print(text)
#                  print(text2)



             # IndexFiles.main(self.getSelectedItem(), text)
            #  print('here')
            #  import sys
            #  sys.argv = ["elasticsearch_loader.py", "--index", "testsdv" , "--type", "testdsvs" , "json" , "michalis.json"]
            #  print(sys.argv)

            #  import time
             
            #  script_descriptor = open("elasticsearch_loader.py" + " --index", "tes" , " --type", "tes" , "json" , "michalis.json")
             
            #  a_script = script_descriptor.read()
            #  sys.argv = ["elasticsearch_loader.py", "--index", "tes" , "--type", "tes" , "json" , "michalis.json"]
         
            #  exec(script_descriptor)
            #import runPython
            #runPython.main(text,text2,getSelectedItem())
           
          