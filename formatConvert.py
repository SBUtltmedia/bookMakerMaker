import csv
import sys
import json
outHeaders={'Title':'Title','Link':'Link','Length':'Duration (seconds)','Lecture No.':'lectureNumber'}
fieldnames = outHeaders.values()
reader = csv.reader(open(sys.argv[1],'r'))

header= reader.next();
outRows={}
for row in reader:
    dict ={}
    for i,x in enumerate(row):
        dict[header[i]] = x
    outRow={}

    for i in outHeaders.keys():
        outRow[outHeaders[i]]=dict[i]
    outRows.setdefault(dict['Week'],[]).append(outRow)

for i in outRows:
    with open("csv/PHY132 - Week "+str(i)+'.csv', 'w') as csvfile:

        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for j in outRows[i]:
            writer.writerow(j)
