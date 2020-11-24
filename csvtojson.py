import csv
import json

file = open("netflix_with_rating2.csv", "r")
dict_reader = csv.DictReader(file)


dict_from_csv = list(dict_reader)
json_from_csv = json.dumps(dict_from_csv)
with open("netflix_with_rating.json2", "w") as outfile: 
    
    outfile.write(json_from_csv)
    
print(json_from_csv)