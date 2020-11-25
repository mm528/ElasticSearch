import sys
print(sys.argv)
import msvcrt as m

def runMain():
    script_descriptor = open("elasticsearch_loader.py")
    a_script = script_descriptor.read()
    sys.argv = ["elasticsearch_loader.py", "--index", "TESTMARIOS" , "--type", "TESTMARIOS" , "json" , "michalis.json"]

    exec(a_script)

input('Wait over here!')

