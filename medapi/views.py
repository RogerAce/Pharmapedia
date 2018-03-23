from django.http import JsonResponse
from django.shortcuts import render
import pandas as pd
import re
dataset = pd.read_csv("medapi/drug.csv", header=None)
#return JsonResponse(returns(list(set(positive)), "G"), safe=False)

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
           # Access - Control - Allow - Origin
            respose=JsonResponse(bfound(name, g[i], i))
            respose["Access-Control-Allow-Origin"]="*"
            return respose
    else:
        return JsonResponse(nbfound(name))#safe=False

def store(request):
    return render(request, "html/text.html")








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


