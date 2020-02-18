#example usage python <nameofProgram> courseInfo.csv

import csv
import os
import sys
import template as t
import json
import copy
import shutil
import getpass
os.chdir(sys.path[0])
BookStem="TeleHealth_"
instructor_netid="mdtmp"
dev_netid=getpass.getuser()
startingLectureDescriptionIndex=1
##title='.'.join(sys.argv[1].split('/')[1][::-1].split(".")[1:])[::-1]
def fitem(item):
    item=item.strip()
    try:
        item=int(item)
    except ValueError:
        pass
    return item

with open(sys.argv[1], 'r') as csvin:
        data = [{k: v for k, v in row.items()}
        for row in csv.DictReader(csvin, skipinitialspace=True)]

bookIndices= set()
for row in data:
    if row["Book"].strip()=="":
        continue
    bookIndices.add(int(row["Book"]))

print sorted(bookIndices)


for idx in bookIndices:
    template=copy.deepcopy(t.template)
    localStorageKey=BookStem+str(idx)
    currentBook=filter(lambda x: x["Book"]==str(idx),data)
    print currentBook

    template["chapters"][0]["title"]=localStorageKey.replace("_"," ")

    pages = {}
    for i,v in enumerate(currentBook):
        lectureNumber = int(v['Lecture No.'])

        if not (lectureNumber  in pages):
            pages[lectureNumber] =[]
        totalsecs = v["Length"]
        if ":" in str(totalsecs):
            min,secs=totalsecs.split(":")[:2]
            totalsecs=int(min)*60+int(secs)
        item = {'type':"video", 'title':v["Title"], 'content':v["Link"], 'duration':totalsecs}
        pages[lectureNumber].append(item)
    template["localStorageKey"]=localStorageKey


    for i in sorted (pages):
        templateChapter=copy.deepcopy(template["chapters"][0])
        templateChapter['content']="localData/TitlePdf/Lecture%d-descriptions.html"%(startingLectureDescriptionIndex)
        templateChapter["pages"]=[]
        for j in pages[i]:
            templateChapter["pages"].append(j)
        template["chapters"].append(templateChapter)
        startingLectureDescriptionIndex+=1
    template["chapters"]=template["chapters"][1:]
    module= json.dumps(template, sort_keys=True,indent=4, separators=(',', ': '))

    src="/Users/%s/Desktop/Apps/bookMaker/Users/dummyUser/Template" %(dev_netid)
    dst="/Users/%s/Desktop/Apps/bookMaker/Users/%s/%s" %(dev_netid,instructor_netid,localStorageKey)
    #os.system("cp - '%s' '%s'" %(src,dst))
    shutil.copytree(src,dst,symlinks=True)
    f = open("%s/module.json"%(dst), "w")
    f.write(module)
#
#
#
#
# template.template["chapters"][0]["title"]=title

#
# with open(sys.argv[1], 'r') as csvin:
#     reader=csv.DictReader(csvin)
#     data={k.strip():[fitem(v)] for k,v in reader.next().items()}
#     for line in reader:
#         for k,v in line.items():
#             k=k.strip()
#             data[k].append(fitem(v))
#
#
# pages = {}
# for i,v in enumerate(data["Link"]):
#     lectureNumber = int( data['lectureNumber'][i])
#
#     if not (lectureNumber  in pages):
#         pages[lectureNumber] =[]
#     totalsecs = data["Duration (seconds)"][i]
#     if ":" in str(totalsecs):
#         print totalsecs
#         min,secs=totalsecs.split(":")
#         totalsecs=int(min)*60+int(secs)
#     item = {'type':"video", 'title':data["Title"][i], 'content':data["Link"][i], 'duration':totalsecs}
#     pages[data['lectureNumber'][i]].append(item)
# template.template["localStorageKey"]=localStorageKey
#
#
# for i in sorted (pages):
#     templateChapter=copy.deepcopy(template.template["chapters"][0])
#     templateChapter['content']="localData/TitlePdf/Lecture%d-descriptions.html"%(i)
#     templateChapter["pages"]=[]
#     for j in pages[i]:
#         templateChapter["pages"].append(j)
#     template.template["chapters"].append(templateChapter)
# template.template["chapters"]=template.template["chapters"][1:]
# module= json.dumps(template.template, sort_keys=True,indent=4, separators=(',', ': '))
#
# src="/Users/evannieuwenh/Desktop/Apps/bookMaker/Cycle 2.1"
# dst="/Users/evannieuwenh/Desktop/Apps/bookMaker/%s" %(title)
# os.system("cp -r '%s' '%s'" %(src,dst))
# f = open("%s/module.json"%(dst), "w")
# f.write(module)
