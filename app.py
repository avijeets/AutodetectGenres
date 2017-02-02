import json
import csv
import sys

def average(tupleSet):
    totalNum = 0
    for pair in tupleSet:
        totalNum += int(pair[1])
    return totalNum/len(tupleSet)

# read json
with open(sys.argv[1]) as json_file:
	data = json.load(json_file)

# dictionary for json categofries
json = [x for x in data]

# import csv
csvFile = open(sys.argv[2])
tables = csv.reader(csvFile)
csvTable = [row for row in tables if row[0] != 'Genre']

#setting up the data structures
empty = list()
for book in json:
	empty.append(dict())
	for row in csvTable: 
		if row[1][1:] in book['description']:
			if row[0] not in empty[-1]:
				empty[-1][row[0]] = dict()
				empty[-1][row[0]]['totalKW'] = 0
				empty[-1][row[0]]['kwTuples'] = set()
				empty[-1][row[0]]['title'] = book['title']
			empty[-1][row[0]]['totalKW'] += book['description'].count(row[1][1:])
			empty[-1][row[0]]['kwTuples'].add((row[1][1:], int(row[2])))

# total num keyword matches * avg point value of the unique matching keyword
scores = list()
for book in empty:
	for key, value in book.items():
		avg = average(book[key]['kwTuples'])
		genreScore = avg * book[key]['totalKW']
		scores.append((key, genreScore, book[key]['title']))
scores.sort(key = lambda tup: tup[1])
# complete score list
print scores[::-1]