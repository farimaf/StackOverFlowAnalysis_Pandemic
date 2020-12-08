import os
import sys
from datetime import datetime
from xml.etree.ElementTree import XML, fromstring

postsXmlPath=sys.argv[1]
postsQuestionsCsvPath=sys.argv[2]
postsAnswersCsvPath=sys.argv[3]


if not os.path.exists(postsQuestionsCsvPath):
    os.makedirs(postsQuestionsCsvPath)

if not os.path.exists(postsAnswersCsvPath):
    os.makedirs(postsAnswersCsvPath)

#headerRow for Questions is: rowId,createDate,score,viewCount,lastEditDate,lastActivityDate,answerCount,commentCount,favoritCount,AcceptedAnswerId
#headerRow for Answers is: rowId,createDate,score,viewCount,lastEditDate,lastActivityDate,answerCount,commentCount,favoritCount,ParentId

# numskipped=0
for file in os.listdir(postsXmlPath):
    if file.endswith(".xml"):
        print("processing "+file+" started")
        xmlFile = open(os.path.join(postsXmlPath,file), 'r', encoding='utf-8')
        postsQuestionsCsvFilePath=os.path.join(postsQuestionsCsvPath,"Questions"+file[0:len(file)-3]+"csv")
        postsAnswersCsvFilePath=os.path.join(postsAnswersCsvPath,"Answers"+file[0:len(file)-3]+"csv")
        fileQuestions=open(postsQuestionsCsvFilePath, 'w')
        fileAnswers=open(postsAnswersCsvFilePath, 'w')
        for line in xmlFile:
            if not line.lstrip().startswith("<row"):
                continue
            row = fromstring(line)
            createDate = row.get('CreationDate')
            if(datetime.strptime(createDate,'%Y-%m-%dT%H:%M:%S.%f')>datetime.strptime('2017-01-01' , '%Y-%m-%d')):
                rowId = row.get('Id')
                score = row.get('Score')
                if (score == None):
                    score = "0"
                viewCount = row.get('ViewCount')
                if(viewCount==None):
                    viewCount="0"
                lastEditDate = row.get('LastEditDate')
                if(lastEditDate==None):
                    lastEditDate=createDate
                lastActivityDate = row.get('LastActivityDate')
                if(lastActivityDate==None):
                    lastActivityDate=createDate
                answerCount = row.get('AnswerCount')#seems that answers do not have answer count
                if (answerCount == None):
                    answerCount = "0"
                commentCount = row.get('CommentCount')
                if (commentCount == None):
                    commentCount = "0"
                favoritCount = row.get('FavoriteCount')#seems that answers do not have favorite count
                if (favoritCount == None):
                    favoritCount = "0"
                # communityOwnedDate = row.get('communityOwnedDate')
                # if(communityOwnedDate==None):
                #     communityOwnedDate="2050-01-01"
                postTypeId = row.get('PostTypeId')
                rowCsv = rowId + "," + createDate + "," + score + "," + viewCount + "," + lastEditDate + "," + lastActivityDate + \
                         "," + answerCount + "," + commentCount + "," + favoritCount #+ "," + communityOwnedDate

                if(postTypeId=="1"):#it's a question
                    acceptedAnswerId=row.get('AcceptedAnswerId')
                    if(acceptedAnswerId==None):
                        acceptedAnswerId=""
                    rowCsv+=","+acceptedAnswerId
                    # print(acceptedAnswerId)
                    fileQuestions.write(rowCsv+"\n")
                elif(postTypeId=="2"):#it's an answer
                    parentId=row.get('ParentId')
                    rowCsv += "," + parentId
                    # print(parentId)
                    fileAnswers.write(rowCsv+"\n")
        print("processing "+file+" finished")
        fileQuestions.close()
        fileAnswers.close()
# print("num skipped bc of acc id of None: "+str(numskipped))
#
# try:
#
# except:
#
#     print(postTypeId)
#     print(score)
#     print(viewCount)
#     print(lastEditDate)
#     print(lastActivityDate)
#     print(answerCount)
#     print(commentCount)
#     print(favoritCount)
#     print(communityOwnedDate)
#     print("-------")