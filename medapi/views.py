from django.http import JsonResponse,HttpResponse;
from django.shortcuts import render
import pandas as pd
import re

dataset = pd.read_csv("medapi/drug.csv", header=None)
dataset2 = pd.read_csv("medapi/Store.csv",header=None)
dataset3 = pd.read_csv("medapi/manufacturer.csv", header=None)

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
    name = request.GET["search"]
    ids = y.index(name)
    lglt = request.GET["lglt"]
    origin = lg, lt = lglt.split(',')
    D = []
    index = []
    gcords = []
    for i in range(lens):  # size of dataset
        if (str(ids) in dataset2.iloc[i, 8]):  # check for meds associated with ith store
            lgs, lts = dataset2.iloc[i, 7].split(',')  # get co-ordinate of ith store
            w1, w2 = 149.9913914007, 111.321543
            k = abs(complex((float(lg) - float(lgs)) * w1, (float(lt) - float(lts)) * w2))
            if (k <= 8):
                D.append(k)  # append distance from store to customer
                index.append(i)  # index of ith store
    mins = []
    if (len(D) < 5):
        m = len(D)
    else:
        m = 5
    for i in range(m):
        smalli = D.index(min(D))  # get the min element and index of dataset2
        mins.append(index[smalli])
        gcords.append(dataset2.iloc[index[smalli], 7])
        del D[smalli]
        del index[smalli]
    Gdata = originf(origin, gcords)
    data = []
    k = 0
    for i in mins:
        name = {"name": dataset2.iloc[i, 1]}
        add = {"add": Gdata[k][0]}
        phone = {"phone": str(dataset2.iloc[i, 4])}
        email = {"email": dataset2.iloc[i, 5]}
        distance = {"distance": Gdata[k][1]}
        time = {"time": Gdata[k][2]}
        k = k + 1
        data.append([name, add, phone, email, distance, time])
    respose = JsonResponse({"header":m,"result":data})  # safe=False
    respose["Access-Control-Allow-Origin"] = "*"
    return respose



def manufacture(request):
    name =request.GET["mft"] #"Ethicon, Inc"  # "all" #
    if name == "all":
        Result = {"header": len(dataset3), "data": list(dataset3.iloc[:, 1].values)}
    else:
        for i in range(len(dataset3)):
            if (name == dataset3.iloc[i, 1]):
                break;
        Result = []
        for j in range(len(dataset3.iloc[i, 2])):
            Result.append(y[j])
        Result = {"header": len(dataset3.iloc[i, 2]), "data": Result}
    respose = JsonResponse(Result) ; # safe=False
    respose["Access-Control-Allow-Origin"] = "*"
    return respose

def banned(resquest):
    file = open("medapi/Banded_Data")
    data = file.readlines()
    file.close()
    for i in range(len(data)):
        data[i] = data[i][:-1]
    title = data[1:len(data)]
    respose = JsonResponse({"title": data[0], "data": title})
    respose["Access-Control-Allow-Origin"] = "*"
    return respose


def Lic(request):
    no = request.GET["no"]
    try:
        z = list(dataset2.iloc[:, 2].values).index(int(no))
        r= {"exist": "1", "email": dataset2.iloc[z, 5]}
    except:
        r={"exist": "0"}
    respose = JsonResponse(r)
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


def originf(origin,des):
    Gdata=[]
    origin=str(origin[0])+","+str(origin[1])
    z=""
    for i in des:
        z=z+i+'|'
    z=z[:-1]
    url="https://maps.googleapis.com/maps/api/distancematrix/json?origins="+origin+"&destinations="+z+"&units=metric&key=AIzaSyBTXSwjuSCwoKTLG0DwI3RhGDAWDQLKENw"
    import json
    import requests
    response = requests.get(url)
    l= json.loads(response.content)
    for i in range(len(l['destination_addresses'])):
         Gdata.append([l['destination_addresses'][i],l['rows'][0]['elements'][i]["distance"]["value"],l['rows'][0]['elements'][0]["duration"]["text"]])
    return Gdata