import os
import sys
from datetime import datetime
from xml.etree.ElementTree import XML, fromstring

votesXmlPath=sys.argv[1]
votesCsvPath=sys.argv[2]

if not os.path.exists(votesCsvPath):
    os.makedirs(votesCsvPath)

#headerRow is "RowId,CreationDate,PostId,VoteType"
# numskipped=0
for file in os.listdir(votesXmlPath):
    if file.endswith(".xml"):
        print("processing "+file+" started")
        xmlFile = open(os.path.join(votesXmlPath,file), 'r', encoding='utf-8')
        votesCsvFilePath=os.path.join(votesCsvPath,file[0:len(file)-3]+"csv")
        with open(votesCsvFilePath, 'w') as csvFile:

            for line in xmlFile:
                if not line.lstrip().startswith("<row"):
                    continue
                row = fromstring(line)
                createDate = row.get('CreationDate')
                if(datetime.strptime(createDate,'%Y-%m-%dT%H:%M:%S.%f')>datetime.strptime('2017-01-01' , '%Y-%m-%d')):
                    rowId = row.get('Id')
                    postId = row.get('PostId')
                    # if(postId==None):
                    #     postId="0"
                    voteTypeId = row.get('VoteTypeId')
                    if (voteTypeId == None):
                        voteTypeId = "0"
                    userId = row.get('UserId')
                    if (userId == None): #userid is only populated for VoteTypeId=5
                        userId = "-1"
                    rowCsv=rowId+","+createDate+","+postId+","+voteTypeId+","+userId
                    csvFile.write(rowCsv+"\n")
        print("processing "+file+" finished")
# print("num skipped bc of acc id of None: "+str(numskipped))
