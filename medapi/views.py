from django.http import JsonResponse
from django.shortcuts import render
import pandas as pd
import re
dataset = pd.read_csv("medapi/drug.csv", header=None)


def index(request):
       return render(request,"html/index.html")
    

def search(request):
    q = request.GET.get("search")
    if not q:

        return
    else:
        name = request.GET['search']  # "Alferon"  # \\

    p = re.compile(name, re.IGNORECASE)
    y = list(dataset.iloc[:, 1].values)

    positive = []
    for i in range(len(y)):
        if (p.match(y[i])):
            positive.append(i)
    if (3 < len(positive)):
        print("BNAME FOUND")
        returns(positive, "B")

    else:
        y = list(dataset.iloc[:, 2].values)
        for i in range(len(y)):
            if (p.match(y[i])):
                positive.append(i)
        print("GNAME FOUND")
        return JsonResponse(returns(list(set(positive)), "G"), safe=False)


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
            for i in range(len(SSplit)):
                try:
                    Infoset.append([SSplit[i], QSplit[i] + " " + USplit[i], CSplit[i]])
                except:
                    print("data created")

            Result.append([BNAME, GNAME, MODE, MANUFACTURER, PRICE, Infoset])
        MED["result"] =Result

    else:
        print("No data found")
    return MED
