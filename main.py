import csv
import os
import sys
import template
import json
import copy
os.chdir(sys.path[0])
title='.'.join(sys.argv[1].split('/')[1][::-1].split(".")[1:])[::-1]
localStorageKey=title.split(" - ")[0]


template.template["chapters"][0]["title"]=title
def fitem(item):
    item=item.strip()
    try:
        item=float(item)
    except ValueError:
        pass
    return item

with open(sys.argv[1], 'r') as csvin:
    reader=csv.DictReader(csvin)
    data={k.strip():[fitem(v)] for k,v in reader.next().items()}
    for line in reader:
        for k,v in line.items():
            k=k.strip()
            data[k].append(fitem(v))


pages = {}
for i,v in enumerate(data["Link"]):
    lectureNumber = int( data['lectureNumber'][i])

    if not (lectureNumber  in pages):
        pages[lectureNumber] =[]
    totalsecs = data["Duration (seconds)"][i]
    if ":" in str(totalsecs):
        print totalsecs
        min,secs=totalsecs.split(":")
        totalsecs=int(min)*60+int(secs)
    item = {'type':"video", 'title':data["Title"][i], 'content':data["Link"][i], 'duration':totalsecs}
    pages[data['lectureNumber'][i]].append(item)
template.template["localStorageKey"]=localStorageKey


for i in sorted (pages):
    templateChapter=copy.deepcopy(template.template["chapters"][0])
    templateChapter['content']="localData/TitlePdf/Lecture%d-descriptions.html"%(i)
    templateChapter["pages"]=[]
    for j in pages[i]:
        templateChapter["pages"].append(j)
    template.template["chapters"].append(templateChapter)
template.template["chapters"]=template.template["chapters"][1:]
module= json.dumps(template.template, sort_keys=True,indent=4, separators=(',', ': '))

src="/Users/evannieuwenh/Desktop/Apps/bookMaker/Cycle 2.1"
dst="/Users/evannieuwenh/Desktop/Apps/bookMaker/%s" %(title)
os.system("cp -r '%s' '%s'" %(src,dst))
f = open("%s/module.json"%(dst), "w")
f.write(module)
