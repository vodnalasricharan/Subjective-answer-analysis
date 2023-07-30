import json
import os
import math
import re
import nav_test
import requests
from fuzzywuzzy import fuzz
import cosine_similarity as keywordVal
import time
import pandas as pd

# TODO- Accuracy prediction library
'''
e = 1
vg = 2
g = 3
o = 4
p = 5
vp = 6

Grammar:
y = 1
n = 0
'''




def givVal(model_answer, keywords, answer, out_of):
    # KEYWORDS =>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    # TODO : Enhacnce this thing
    if (len(answer.split())) <= 5:
        return 0
    #
    # count = 0
    # keywords_count = len(keywords)
    # for i in range(keywords_count):
    #     if keywords[i] in answer:
    #         # print (keywords[i])
    #         count = count + 1
    # k = 0
    # if count == keywords_count:
    #     k = 1
    # elif count == (keywords_count - 1):
    #     k = 2
    # elif count == (keywords_count - 2):
    #     k = 3
    # elif count == (keywords_count - 3):
    #     k = 4
    # elif count == (keywords_count - 4):
    #     k = 5
    # elif count == (keywords_count - 5):
    #     k = 6
    k = keywordVal.givKeywordsValue(model_answer, answer)
    # print("checkkkkkk", k)

    # GRAMMAR =>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

    req = requests.get("https://api.textgears.com/check.php?text=" + answer + "&key=JmcxHCCPZ7jfXLF6")
    no_of_errors=0
    if not (req.json().get('errors') is None):
    	no_of_errors = len(req.json()['errors'])

    if no_of_errors > 5 or k == 6:
        g = 0
    else:
        g = 1

    # QST =>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    # print("fuzz1 ratio: ", fuzz.ratio(model_answer, answer))
    q = math.ceil(fuzz.token_set_ratio(model_answer, answer)/ 10)
    if q>=10:
        q = q-1
    q= 10 - q
    # print("Keywords : ", k)
    # print("Grammar  : ", g)
    # print("QST      : ", q)

    predicted = nav_test.predict(k, g, q)
    # Mathematical model->
    # predicted / 10
    # what?	/ out_of
    result = predicted * out_of / 10
    return result[0]

dat=[]
directory = "../temp"
for filename in os.listdir(directory):

    f = os.path.join(directory, filename)

    if os.path.isfile(f):
        x = open(f, 'r', encoding="cp866")
        dat.append(json.load(x))



model_answer1 = dat[0]['answer']
out_of1 = dat[0]['out_of']
keywords1 =dat[0]['keywords']
keywords1 = re.findall(r"[a-zA-Z]+", keywords1)

model_answer2 = dat[1]['answer']
out_of2 = dat[1]['out_of']
keywords2 =dat[1]['keywords']
keywords2 = re.findall(r"[a-zA-Z]+", keywords2)

model_answer3 = dat[2]['answer']
out_of3 = dat[2]['out_of']
keywords3 =dat[2]['keywords']
keywords3 = re.findall(r"[a-zA-Z]+", keywords3)


keywords=[keywords1,keywords2,keywords3]
directory="../DataSetCollectorFlaskApp/data"
result=0
model_answers=[model_answer1,model_answer2,model_answer3]
out_ofs=[out_of1,out_of2,out_of3]
studentReport=[]
StudentEmail=[]
StudentMarks=[]
marksperQ=[]
Totalmarks=[]

for filename in os.listdir(directory):
    f = os.path.join(directory, filename)
    if os.path.isfile(f):
        x=open(f,encoding="cp866")
        data = json.load(x)
        result=0
        answers=[data['a1'],data['a2'],data['a3']]
        results = []
        total=0
        #print(data["email"])
        for xx in range(3):
            results.append(result)
            #print("question : "+str(xx))
            result =result+ givVal(model_answers[xx], keywords[xx], answers[xx], out_ofs[xx])
            total = total+out_ofs[xx]
        StudentMarks.append(result)
        StudentEmail.append(data["email"])
        marksperQ.append(results)
        Totalmarks.append(total)


ToatalReport=pd.DataFrame(list(zip(StudentEmail,StudentMarks,Totalmarks)))
ToatalReport.columns = ['Student Name','Marks obtained' , 'Total marks']
ToatalReport.index +=1
print(ToatalReport)

# for filename in os.listdir(directory):
#     f = os.path.join(directory, filename)
#     if os.path.isfile(f):
#         x=open(f,encoding='cp866')
#         data = json.load(x)
#         print("\n\n" + data['email'])
#         answer1=data['a1']
#         result1 = givVal(model_answer1, keywords1, answer1, out_of1)
#         print("Marks for question 1 : " + str(result1)+ " out of :"+str(out_of1))
#         answer2 = data['a2']
#         result2 = givVal(model_answer2, keywords2, answer2, out_of2)
#         print("Marks for question 2 : " + str(result2) + " out of :" + str(out_of2))
#         answer3 = data['a3']
#         result3 = givVal(model_answer3, keywords3, answer3, out_of3)
#         print("Marks for question 3 : " + str(result3) + " out of :" + str(out_of3))

