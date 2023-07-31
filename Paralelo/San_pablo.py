from selenium import webdriver as wd
from time import time,sleep
from datetime import date
import pandas as pd
import numpy as npy
import re
cat = pd.read_csv(r'C:\Users\APPWHERE\Desktop\CompendioStatus.csv',encoding = 'latin1')
cat = cat.fillna("aslkmvodnvoa")
def openbrowser():
    chrome_options = wd.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    driver = wd.Chrome(r'C:\Farmaceutica\chromedriver',options=chrome_options)
    return driver
def closeall():
    cd = 0
    t = True
    while t:
        try:
            driver.quit()
            cd += 1
            print("driver "+str(cd)+" closed")
        except:
            t = False
d_a = [["á","a"],["ó","o"],["í","i"],["é","e"],["ú","u"]]
def noacentos(txt):
    for i in d_a:
        txt = txt.replace(i[0],i[1])
    return txt
#Farmacias San Pablo
san_pablo_searchtest=[]
start = time()
hoy = str(date.today())
#driver = openbrowser()
driver = wd.Chrome(r'C:\Farmaceutica\chromedriver.exe')
finds = []
size = ["piez","amp","cáp","cap","tab","gra","past","jara","mili","ml","g","kg","iny","par","sob","jug",
        "ung","ov","óv","com","sus","sobr"]
cont = ["mili","mg","ml","gr","g"]
seps = [".",",",";","/","-"]
def checkeo(elems):
    #print(elems)
    prod=elems[0][0]
    price_max=max(float(x[1].replace("$","").replace(" MXN","").replace(",","")) for x in elems)
    price_min=min(float(x[1].replace("$","").replace(" MXN","").replace(",","")) for x in elems)
    obsrv=len(elems)
    if obsrv > 1:
        status="3"
    elif obsrv == 1:
        status="1"
    #print(["check",prod,price_min,price_max,status])
    toset(prod,price_min,price_max,obsrv,status)
    return 
def toset(ID,price_min,price_max,obs,status):
    san_pablo_searchtest.append([str(ID),price_min,price_max,obs,status])
    return
for entry in range(cat.shape[0]):
    sz = 0
    br = 0
    ac = 0
    d = cat.values[entry]
    t = d[2]
    #print([d[3],d[4]])
    pres = re.findall("\d+",d[3])
    if pres:
        pres = "".join(pres)
    else:
        pres = " "
    comp = re.match(".*\d+",d[4])
    if comp:
        comp = comp.group(0)
    else:
        comp = " "
    #print([pres,comp])
    if d[2] == "ANTIFLUDES": t = "ANTIFLU-DES"
    if d[2] == "ANTIFLUDES PEDIÁTRICO": t = "ANTIFLU-DES PEDIÁTRICO"
    if d[2] == "DIMETAPP INFANTIL": t = "DIMETAP INFANTIL"
    driver.get('https://www.farmaciasanpablo.com.mx/search/?text='+t)
    if d[2] == "CLAVULIN 12H": t = "CLAVULIN"
    if d[2] == "DIMETAPP PEDIÁTRICO": t = "DIMETAP PEDIÁTRICO"
    if d[2] == "MOTRIN PEDIÁTRICO FRESA FRAMBUESA": t = "MOTRIN PEDIÁTRICO"
    if d[2] == "MOTRIN INFANTIL FRESA FRAMBUESA": t = "MOTRIN INFANTIL"
    if d[2] == "BENZATINA BENCILPENICILINA 1200000": t = "Bencilpenicilina Benzatinica 1200000"
    if d[2] == "PTI PANTOPRAZOL": t = "PANTOPRAZOL"
    if d[2] == "VICK VITAPYRENA manzana con canela": t = "VICK VITAPYRENA manzana canela"
    if d[2] == "ADVIL INFANTIL FRUTAS": t = "ADVIL INFANTIL"
    if d[2] == "ANTIFLUDES": t = "ANTIFLU-DES"
    if d[2] == "EVOCS 111": t = "EVOCS III"
    if d[2] == "CEFURACET 7D": t = "CEFURACET"
    if d[2] == "PEINE PARA LOS PIOJOS": t = "PEINE PARA PIOJOS"
    if d[2] == "LADEXEL": t = "LADEXGEL"
    if d[2] == "LARITROL Ex": t = "LARITOL Ex"
    data = [driver.find_elements_by_xpath('//*[@class="item-title"]'),
            driver.find_elements_by_xpath('//*[@class="item-subtitle"]'),
            driver.find_elements_by_xpath('//*[@class="item-prize"]')]
    for i in range(len(data[0])):
        s_r = data[0][i].text+" "+data[1][i].text
        s_r = s_r.lower()
        br = 1
        #print([d[2],s_r])
        for k in t.split(' '):
            aux = k.lower()
            found = s_r
            for s in seps:
                aux = aux.replace(s,"")
                found = found.replace(s,"")
            aux = noacentos(aux)
            found = noacentos(found)
            #print([aux,found])
            if aux == "pediatrico": aux = "pediat"
            if aux == "fastgel": aux = "fast gel"
            if aux.lower() not in found:
                br = 0
            #print([aux.lower(),found,br])
        if br == 1:
            sz = 0
            if d[3] != "aslkmvodnvoa": 
                for k in size:
                    presentacion = " ".join([pres,k]).strip()
                    if presentacion.lower() in found:
                        sz = 1
            else:
                sz = 1
            for k in cont:
                compuesto = " ".join([comp,k])
                if compuesto.lower() in s_r:
                    ac = 1
        #print([d[2],pres,comp,found])
        if [br,sz,ac] == [1,1,1]:
            #finds.append([d[0],data[2][i].text,"1"])
            price=float(data[2][i].text.replace("$","").replace(" MXN","").replace(",",""))
            toset(d[0],price,price,"1","1")
            finds.clear()
            break
        elif [br,sz] == [1,1] or [br,ac] == [1,1] or [sz,ac] == [1,1] :
            finds.append([d[0],data[2][i].text,"3"])
        #print([br,sz,ac])
    if len(finds)>0:
        checkeo(finds)
        finds.clear()
    #print(str(entry))
driver.quit()
