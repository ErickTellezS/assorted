from selenium import webdriver as wd
from time import time,sleep
from datetime import date
import pandas as pd
import numpy as npy
import re
import psycopg2


def make_a_cat():
    conn = psycopg2.connect(user="postgres", password="0123456789", host="127.0.0.1", port="5432", database="Farmacias")
    curs = conn.cursor()
    curs.execute("SELECT * FROM med_base")
    outcat = curs.fetchall()
    curs.close()
    conn.close()
    outframe = pd.DataFrame(outcat)
    outframe.columns = ["ID", "EAN", "Nombre", "Presentación", "Compuesto"]
    return outframe


def noacentos(txt):
    d_a = [["á", "a"], ["ó", "o"], ["í", "i"], ["é", "e"], ["ú", "u"]]
    for i in d_a:
        txt = txt.replace(i[0],i[1])
    return txt


def to_db():
    #print('San Pablo')
    cat = make_a_cat()
    cat = cat.fillna("aslkmvodnvoa")

    '''start = time()
    hoy = date.today().strftime("%d/%m/%Y")
    chrome_options = wd.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    driver = wd.Chrome('/home/erick/PycharmProjects/chromedriver', options=chrome_options)
    finds = []
    size = ["piez", "amp", "cáp", "cap", "tab", "gra", "past", "jara", "mili", "ml", "g", "kg", "iny", "par", "sob",
            "jug",
            "ung", "ov", "óv", "com", "sus", "sobr"]
    cont = ["mili", "mg", "ml", "gr", "g"]
    seps = [".", ",", ";", "/", "-"]
    for entry in range(cat.shape[0]):
        sz = 0
        br = 0
        ac = 0
        d = cat.values[entry]
        t = d[2]
        pres = re.findall("\d+", d[3])
        if pres:
            pres = "".join(pres)
        else:
            pres = " "
        comp = re.match(".*\d+", d[4])
        if comp:
            comp = comp.group(0)
        else:
            comp = " "
        if d[2] == "ANTIFLUDES": t = "ANTIFLU-DES"
        if d[2] == "ANTIFLUDES PEDIÁTRICO": t = "ANTIFLU-DES PEDIÁTRICO"
        if d[2] == "DIMETAPP INFANTIL": t = "DIMETAP INFANTIL"
        driver.get('https://www.farmaciasanpablo.com.mx/search/?text=' + t)
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
            s_r = data[0][i].text + " " + data[1][i].text
            s_r = s_r.lower()
            br = 1
            for k in t.split(' '):
                aux = k.lower()
                found = s_r
                for s in seps:
                    aux = aux.replace(s, "")
                    found = found.replace(s, "")
                aux = noacentos(aux)
                found = noacentos(found)
                if aux == "pediatrico": aux = "pediat"
                if aux == "fastgel": aux = "fast gel"
                if aux.lower() not in found:
                    br = 0
            if br == 1:
                sz = 0
                if d[3] != "aslkmvodnvoa":
                    for k in size:
                        presentacion = " ".join([pres, k]).strip()
                        if presentacion.lower() in found:
                            sz = 1
                else:
                    sz = 1
                for k in cont:
                    compuesto = " ".join([comp, k])
                    if compuesto.lower() in s_r:
                        ac = 1
            if [br, sz, ac] == [1, 1, 1]:
                finds.append([d[0], data[2][i].text, "1"])
                break
            elif [br, sz] == [1, 1] or [br, ac] == [1, 1] or [sz, ac] == [1, 1]:
                finds.append([d[0], data[2][i].text, "3"])
    driver.quit()
    sanpablo = pd.DataFrame(finds)
    sanpablo[1] = sanpablo[1].str.replace("$", "").str.replace(" MXN", "").str.replace(",", "").astype(float)
    sanpablo.columns = ["ID", "precio", "match"]
    optimatch = sanpablo.groupby(["ID"]).agg({"match": npy.min})
    c_sanpablo = optimatch.merge(sanpablo, left_on="ID", right_on="ID", how="right")
    c_sanpablo = c_sanpablo[c_sanpablo["match_x"] == c_sanpablo["match_y"]]
    cnt = c_sanpablo[c_sanpablo["precio"] > 0].groupby("ID").count()["match_x"]
    cSP = c_sanpablo.merge(cnt, left_on="ID", right_on="ID", how="left")
    maxmin_sp = cSP.groupby(["ID"]).agg({'precio': [npy.min, npy.max]})
    cSPmm = cSP.merge(maxmin_sp, left_on="ID", right_on="ID", how="right")
    cSPmm.columns = ["ID", "status", "precio", "min_status", "obs", "min", "max"]
    cSPmm = cSPmm[["ID", "status", "obs", "min", "max"]]
    catalogo = make_a_cat()
    SP_csv = catalogo.merge(cSPmm, left_on="ID", right_on="ID", how="left")
    SP_csv.columns = ['ID', 'EAN', 'Nombre', 'Presentación', 'Compuesto',
                      'status', 'obs', 'min', 'max']
    SP_csv["status"] = SP_csv["status"].fillna(2)
    SP_csv["obs"] = SP_csv["obs"].fillna(0)
    SP_csv["min"] = SP_csv["min"].fillna(0)
    SP_csv["max"] = SP_csv["max"].fillna(0)
    SP_csv["Compuesto"] = SP_csv["Compuesto"].fillna(" ")
    SP_csv["Presentación"] = SP_csv["Presentación"].fillna(" ")
    SP_csv = SP_csv.drop_duplicates()
    SP_csv = SP_csv.sort_values(by="ID")
    SP_csv["fecha"] = hoy
    SP_csv["status"] = SP_csv.apply(lambda x: 1 if x[6] == 1 else x[5], axis=1)

    connection = psycopg2.connect(user="postgres", password="0123456789", host="127.0.0.1", port="5432",
                                  database="Farmacias")
    cursor = connection.cursor()
    for entry in range(SP_csv.shape[0]):
        d = SP_csv.values[entry]
        id_ = d[0]
        fecha_ = d[9]
        enc_ = d[6]
        min_ = d[7]
        max_ = d[8]
        stat_ = d[5]
        to_fill = [id_, fecha_, enc_, min_, max_, stat_]
        cursor.execute("INSERT INTO san_pablo VALUES {}".format(tuple(to_fill)))
    connection.commit()
    cursor.close()
    connection.close()

    print((time() - start) / 60)'''

    print('Del Ahorro')
    start = time()
    hoy = date.today().strftime("%d/%m/%Y")
    chrome_options = wd.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    driver = wd.Chrome('/home/erick/PycharmProjects/chromedriver', options=chrome_options)
    driver.get('https://www.fahorro.com')
    finds = []
    size = ["piez", "amp", "cáp", "cap", "tab", "gr", "past", "jara", "mili", "ml", "g", "kg", "iny", "par", "sob",
            "jug", "ung"]
    cont = ["mili", "mg", "ml", "gr", "g"]
    seps = [".", ",", ";", "/", "-"]
    for entry in range(cat.shape[0]):
        print(entry)
        sz = 0
        br = 0
        ac = 0
        d = cat.values[entry]
        t = d[2]
        obj = False
        pres = re.findall("\d+", d[3])
        if pres:
            pres = "".join(pres)
        else:
            pres = " "
        comp = re.match(".*\d+", d[4])
        if comp:
            comp = comp.group(0)
        else:
            comp = " "
        while not obj:
            try:
                search = driver.find_element_by_xpath('//*[@id="search"]')
                obj = True
            except:
                pass
        search.clear()
        search.send_keys(t)
        driver.find_element_by_xpath('//*[@type = "submit"]').click()
        data = [driver.find_elements_by_xpath("//*[@class='product-shop']"),
                driver.find_elements_by_xpath("//*[@class='price-box']")]
        for i in range(len(data[0])):
            s_r = data[0][i].text
            s_r = s_r.lower()
            br = 1
            for k in t.split(' '):
                aux = k.lower()
                found = s_r
                for s in seps:
                    aux = aux.replace(s, "")
                    found = found.replace(s, "")
                aux = noacentos(aux)
                found = noacentos(found)
                if aux.lower() not in found.replace(" ", ""):
                    br = 0
            if br == 1:
                sz = 0
                if d[3] != "aslkmvodnvoa":
                    for k in size:
                        presentacion = " ".join([pres, k])
                        if presentacion.lower() in found:
                            sz = 1
                else:
                    sz = 1
                for k in cont:
                    compuesto = " ".join([comp, k])
                    if compuesto.lower() in s_r:
                        ac = 1
            if [br, sz, ac] == [1, 1, 1]:
                finds.append([d[0], data[1][i].text, "1"])
                break
            elif [br, sz] == [1, 1] or [br, ac] == [1, 1] or [sz, ac] == [1, 1]:
                finds.append([d[0], data[1][i].text, "3"])
            sleep(2.2)
    driver.quit()
    fahorro = pd.DataFrame(finds)
    fahorro[1] = fahorro[1].map(lambda x: x.split('\n')[0])
    fahorro[1] = fahorro[1].str.replace("$", "").str.replace(" MXN", "").str.replace(",", "").astype(float)
    fahorro.columns = ["ID", "precio", "match"]
    optimatch = fahorro.groupby(["ID"]).agg({"match": npy.min})
    c_fahorro = optimatch.merge(fahorro, left_on="ID", right_on="ID", how="right")
    c_fahorro = c_fahorro[c_fahorro["match_x"] == c_fahorro["match_y"]]
    cnt = c_fahorro[c_fahorro["precio"] > 0].groupby("ID").count()["match_x"]
    cFA = c_fahorro.merge(cnt, left_on="ID", right_on="ID", how="left")
    maxmin_fa = cFA.groupby(["ID"]).agg({'precio': [npy.min, npy.max]})
    cFAmm = cFA.merge(maxmin_fa, left_on="ID", right_on="ID", how="right")
    cFAmm.columns = ["ID", "status", "precio", "min_status", "obs", "min", "max"]
    cFAmm = cFAmm[["ID", "status", "obs", "min", "max"]]
    catalogo = make_a_cat()
    FA_csv = catalogo.merge(cFAmm, left_on="ID", right_on="ID", how="left")
    FA_csv.columns = ['ID', 'EAN', 'Nombre', 'Presentación', 'Compuesto',
                      'status', 'obs', 'min', 'max']
    FA_csv["status"] = FA_csv["status"].fillna(2)
    FA_csv["obs"] = FA_csv["obs"].fillna(0)
    FA_csv["min"] = FA_csv["min"].fillna(0)
    FA_csv["max"] = FA_csv["max"].fillna(0)
    FA_csv["Compuesto"] = FA_csv["Compuesto"].fillna(" ")
    FA_csv["Presentación"] = FA_csv["Presentación"].fillna(" ")
    FA_csv = FA_csv.drop_duplicates()
    FA_csv = FA_csv.sort_values(by="ID")
    FA_csv["fecha"] = hoy
    FA_csv["status"] = FA_csv.apply(lambda x: 1 if x[6] == 1 else x[5], axis=1)

    connection = psycopg2.connect(user="postgres", password="0123456789", host="127.0.0.1", port="5432",
                                  database="Farmacias")
    cursor = connection.cursor()
    for entry in range(FA_csv.shape[0]):
        d = FA_csv.values[entry]
        id_ = d[0]
        fecha_ = d[9]
        enc_ = d[6]
        min_ = d[7]
        max_ = d[8]
        stat_ = d[5]
        to_fill = [id_, fecha_, enc_, min_, max_, stat_]
        cursor.execute("INSERT INTO del_ahorro VALUES {}".format(tuple(to_fill)))
    connection.commit()
    cursor.close()
    connection.close()

    print((time() - start) / 60)

