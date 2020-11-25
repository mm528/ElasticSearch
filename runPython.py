#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import sys
#print(nameIndex + " " + typeName + " " +path )
script_descriptor = open("elasticsearch_loader.py")
a_script = script_descriptor.read()
sys.argv = ["-i elasticsearch_loader.py", "--index","michalis", "--type", "michalis" , "json" , "michalis.json"]

exec(a_script)







