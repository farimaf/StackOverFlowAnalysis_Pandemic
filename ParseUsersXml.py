import os
import sys
from datetime import datetime
from xml.etree.ElementTree import XML, fromstring

usersXmlPath=sys.argv[1]
usersCsvPath=sys.argv[2]

if not os.path.exists(usersCsvPath):
    os.makedirs(usersCsvPath)

headerRow="AccId,CreateDate,LastAccessDate,ViewsNum,UpVotes,DownVotes"

for file in os.listdir(usersXmlPath):
    if file.endswith(".xml"):
        print("processing "+file+" started")
        xmlFile = open(os.path.join(usersXmlPath,file), 'r', encoding='utf-8')
        usersCsvFilePath=os.path.join(usersCsvPath,file[0:len(file)-3]+"csv")
        with open(usersCsvFilePath, 'w') as csvFile:
            csvFile.write(headerRow+"\n")
            for line in xmlFile:
                if not line.lstrip().startswith("<row"):
                    continue
                row = fromstring(line)
                createDate = row.get('CreationDate')
                if(datetime.strptime(createDate,'%Y-%m-%dT%H:%M:%S.%f')>datetime.strptime('2017-01-01' , '%Y-%m-%d')):
                    lastAccessDate = row.get('LastAccessDate')
                    viewsNum = row.get('Views')
                    upVotes = row.get('UpVotes')
                    downVotes = row.get('DownVotes')
                    accId = row.get('AccountId')
                    rowCsv=accId+","+createDate+","+lastAccessDate+","+viewsNum+","+upVotes+","+downVotes
                    csvFile.write(rowCsv+"\n")
        print("processing "+file+" finished")