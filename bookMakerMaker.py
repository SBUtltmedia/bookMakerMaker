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
BookStem="PHY132_Summer_"
instructor_netid="themmick"
lastBookType=""
# dev_netid=getpass.getuser()

##title='.'.join(sys.argv[1].split('/')[1][::-1].split(".")[1:])[::-1]
bookMakerPath="../apache2/htdocs/bookMaker/"
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




for idx in bookIndices:
    startingLectureDescriptionIndex=1
    template=copy.deepcopy(t.template)
    localStorageKey=BookStem+str(idx)
    currentBook=filter(lambda x: x["Book"]==str(idx),data)


    template["chapters"][0]["title"]=localStorageKey.replace("_"," ")

    pages = {}
    for i,v in enumerate(currentBook):
        print(v)
        lectureNumber = int(v['Lecture No.'])

        if not (lectureNumber  in pages):
            pages[lectureNumber] =[]
        totalsecs = v["Length"]
        if ":" in str(totalsecs):
            min,secs=totalsecs.split(":")[:2]
            totalsecs=int(min)*60+int(secs)
        item = {'type':"video", 'title':v["Title"], 'description':v["Description"],'content':v["Link"], 'duration':totalsecs}
        pages[lectureNumber].append(item)
    template["localStorageKey"]=localStorageKey


    for i in sorted (pages):
        # print pages
        templateChapter=copy.deepcopy(template["chapters"][0])
        templateChapter['content']="sourceFiles/html/descriptions.html#%s"%(startingLectureDescriptionIndex)
        templateChapter["pages"]=[]
        for j in pages[i]:
            templateChapter["pages"].append(j)
        template["chapters"].append(templateChapter)
        startingLectureDescriptionIndex+=1
    template["chapters"]=template["chapters"][1:]
    module= json.dumps(template, sort_keys=True,indent=4, separators=(',', ': '))
    if v["Book Type"]!=lastBookType:
        bookTypeOffset=idx-1
    lastBookType=v["Book Type"]
    src="%s/Users/dummyUser/Template" %(bookMakerPath)
    dst="%s/Users/%s/%s%s_%s" %(bookMakerPath,instructor_netid,BookStem,v["Book Type"], idx-bookTypeOffset)
    #os.system("cp - '%s' '%s'" %(src,dst))
    #shutil.rmtree(dst)
    try:
        shutil.copytree(src,dst,symlinks=True)
    except:
        print("Directory exists, creating new module.json")
    f = open("%s/module.json"%(dst), "w")
    f.write(module)
