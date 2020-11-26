#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import sys
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import QMessageBox
#print(nameIndex + " " + typeName + " " +path )
script_descriptor = open("elasticsearch_loader.py")
a_script = script_descriptor.read()
sys.argv = ["-i elasticsearch_loader.py", "--index","michalis", "--type", "michalis" , "json" , "michalis.json"]

# QCoreApplication.quit()
# input("eNTER")
msg = QMessageBox()
msg.setWindowTitle("Will exit the system")


exec(a_script)

msg = QMessageBox()
msg.setWindowTitle("Will exit the system")

#QCoreApplication.quit()









