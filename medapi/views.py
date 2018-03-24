from django.http import JsonResponse
from django.shortcuts import render
import pandas as pd
import re

dataset = pd.read_csv("medapi/drug.csv", header=None)
dataset2 = pd.read_csv("medapi/store.csv",header=None)
lenm=len(dataset)
lens=len(dataset2)

def index(request):
       return render(request,"html/index.html")


y = list(dataset.iloc[:, 1].values)
g = list(dataset.iloc[:, 2].values)
length = len(y);


def search(request):
    name = request.GET['search']
    name = " ".join(name.split()).title()
    for i in range(length):
        if (name == y[i]):
           #Access-Control-Allow-Origin
            respose=JsonResponse(bfound(name, g[i], i))
            respose["Access-Control-Allow-Origin"]="*"
            return respose
    else:
        respose = JsonResponse(nbfound(name))#safe=False
        respose["Access-Control-Allow-Origin"]="*"
        return respose


def store(request):
    name=request.GET["search"]
    ids=y.index(name)
    lglt=request.GET["lglt"]
    lg,lt=lglt.split(',')
    D=[]
    index=[]
    for i in range(lens):
        if(str(ids) in dataset2.iloc[i,8]):
            lgs,lts =dataset2.iloc[i,7].split(',')
            D.append(abs(complex( float(lg)-float(lts),float(lt)-float(lts) )))
            index.append(i)
    mins=[]
    if(len(D)<5):
        m=len(D)
    else:
        m=5
    for i in range(m):
        smalli=D.index(min(D))
        mins.append(index[smalli])
        del D[smalli]
        del index[smalli]
    data=[]
    for i in mins:
        name={"name":dataset2.iloc[i,1]}
        cord={"coord":dataset2.iloc[i,7]}
        add={"add":dataset2.iloc[i,3]}
        phone={"phone":str(dataset2.iloc[i,4])}
        email={"email":dataset2.iloc[i,5]}
        data.append([name,cord,add,phone,email])
    respose = JsonResponse({"header":m,"result":data})  # safe=False
    respose["Access-Control-Allow-Origin"] = "*"
    return respose






def returns(positive, N):
    MED = {}
    MED["header"] = [len(positive), N]

    if (len(positive)):
        Result = []
        for i in positive:

            BNAME = dataset.iloc[i, 1]
            GNAME = dataset.iloc[i, 2]
            MODE = dataset.iloc[i, 3]
            MANUFACTURER = dataset.iloc[i, 4]
            PRICE = str(dataset.iloc[i, 9])
            SALTS = dataset.iloc[i, 5]
            QUANTITY = str(dataset.iloc[i, 6])
            UNIT = dataset.iloc[i, 7]
            CLASS = dataset.iloc[i, 8]

            SSplit = SALTS.split(';')
            QSplit = QUANTITY.split(';')
            USplit = UNIT.split(';')
            CSplit = CLASS.split(',')
            Infoset = []
            for j in range(len(SSplit)):
                try:
                    Infoset.append([SSplit[j], QSplit[j] + " " + USplit[j], CSplit[j]])
                except Exception as ex:
                    break

            Result.append([BNAME, GNAME, MODE, MANUFACTURER, PRICE, Infoset])
        MED["result"] =Result

    else:
        print("No data found")
    return MED


def bfound(name, gname, ix):
    positive = [ix]
    salts = g[ix].split(",")
    for i in range(length):
        temp = g[i].split(',')
        for j in temp:
            if (j not in salts):
                break
        else:
            positive.append(i)

    return returns(list(set(positive)), "B")


def nbfound(name):
    positive = []
    p = re.compile(name, re.IGNORECASE)

    for i in range(length):
        if (p.match(y[i])):
            positive.append(i)
    if (len(positive) < 10):
        for i in range(length):
            if (p.match(g[i])):
                positive.append(i)
    return returns(list(set(positive)), "G")


