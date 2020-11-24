import csv
import json
import re
file = open("netflix_titles.csv", "r", encoding='UTF8') #Edw to diavazi me UTF8 (SIMANTIKO)
dict_reader = csv.DictReader(file)

dict_from_csv = list(dict_reader)
json_from_csv = json.dumps(dict_from_csv)
with open('netflix_titles.csv','rt',encoding='UTF8')as f:
  data = csv.reader(f,delimiter = '\t')
  for row in data:
        #print(row)
        delchars = ''.join(c for c in map(chr, range(256)) if not c.isalnum())
        re.sub(r'\delchars+', '', 'skjbfaesjfbcs')
        letters_only = re.sub("½", "", row[0])
        letters_only = re.sub("ï", "", letters_only)
        letters_only = re.sub("#", "", letters_only)
        letters_only = re.sub("NaN", "", letters_only) ###>>>> AFAIROUME OLA TA PERITTA P DEN THELOUME STO JSON!!

        #print(letters_only)
        with open("michalis.json", "w") as outfile:
          outfile.write(json_from_csv)


# dict_from_csv = list(dict_reader)
# json_from_csv = json.dumps(dict_from_csv)
# with open("michalis.json", "w") as outfile: 
#     # outfile.write('[')
#     outfile.write(json_from_csv)
#     # outfile.write(']')
# print(json_from_csv)