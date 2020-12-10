import os
import sys
from datetime import datetime
from xml.etree.ElementTree import XML, fromstring

commentsXmlPath=sys.argv[1]
commentsCsvPath=sys.argv[2]

if not os.path.exists(commentsCsvPath):
    os.makedirs(commentsCsvPath)

#headerRow is "RowId,CreationDate,PostId,Score,UserId"
# numskipped=0
for file in os.listdir(commentsXmlPath):
    if file.endswith(".xml"):
        print("processing "+file+" started")
        xmlFile = open(os.path.join(commentsXmlPath,file), 'r', encoding='utf-8')
        commentsCsvFilePath=os.path.join(commentsCsvPath,file[0:len(file)-3]+"csv")
        with open(commentsCsvFilePath, 'w') as csvFile:

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
                    score = row.get('Score')
                    # if (score == None):
                    #     score = "0"
                    userId = row.get('UserId')
                    # if (userId == None):
                    #     userId = "-1"
                    rowCsv=rowId+","+createDate+","+postId+","+score+","+userId
                    csvFile.write(rowCsv+"\n")
        print("processing "+file+" finished")
# print("num skipped bc of acc id of None: "+str(numskipped))
