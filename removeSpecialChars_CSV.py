import csv

with open('netflix_with_rating3.csv', "rb",  encoding= UTF8) as infile, open('netflix_with_rating2.csv', "wb") as outfile:
    reader = csv.reader(infile)
    writer = csv.writer(outfile)
    conversion = set('_"/.$')
    for row in reader:
        newrow = [''.join('_' if c in conversion else c for c in entry) for entry in row]
        writer.writerow(newrow)

