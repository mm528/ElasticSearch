
import time
import sys
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import QMessageBox
import chardet




with open ("C:/Users/motis/Desktop/finallyProject/ElasticSearch/password.txt", 'rt') as myfile:
      for myline in myfile: 
          getAsstring = myline
          x = getAsstring.split()
          print(x)

        

#print(nameIndex + " " + typeName + " " +path )
script_descriptor = open("elasticsearch_loader.py")
a_script = script_descriptor.read()
sys.argv = ["-i elasticsearch_loader.py", "--index", "imdb", "--type", "imdb", "json" , "IMDB.json"] 
#sys.argv = ["-i elasticsearch_loader.py", "--index", x[0], "--type", x[1], "json" , x[2]] >>>>>> storing into a txt file and passing over here the data
#but it wasnt able fully functional 

# QCoreApplication.quit()
# input("eNTER")

exec(a_script)

msg = QMessageBox()

#QCoreApplication.quit()









