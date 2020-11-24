import csv
import json

file = open("netflix_with_rating.csv", "r", encoding='UTF8') #Edw to diavazi me UTF8 (SIMANTIKO)
dict_reader = csv.DictReader(file)


dict_from_csv = list(dict_reader)
json_from_csv = json.dumps(dict_from_csv)
with open("michalis.json", "w") as outfile: 
    # outfile.write('[')
    outfile.write(json_from_csv)
    # outfile.write(']')
print(json_from_csv)