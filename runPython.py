import sys
print(sys.argv)

import time

script_descriptor = open("elasticsearch_loader.py")
a_script = script_descriptor.read()
sys.argv = ["elasticsearch_loader.py", "--index", "testsdvewf" , "--type", "testdswefvs" , "json" , "michalis.json"]

exec(a_script)


