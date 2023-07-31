import re
from unidecode import unidecode
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.common import exceptions
from selenium.webdriver.chrome.options import Options as COptions


def look_chedraui(medicamento):
    p_prod = 'alt=".*?"'
    p_prec = '\\$.*?\\</div'

    options = COptions()
    options.headless = True
    options.add_argument('--no-proxy-server')

    driver = webdriver.Chrome(executable_path='/home/erick/PycharmProjects/chromedriver', options=options)
    wait = WebDriverWait(driver, 600)

    command = 'https://www.chedraui.com.mx/search?text=####&method=enter'
    if medicamento in ['motrin pediatrico', 'motrin infantil', 'antifludes pediatrico', 'reddy adulto']:
        searchmed = medicamento.replace('pediatrico', 'ped').replace('infantil', 'inf').replace(' ', '%20')
    elif medicamento == 'ferranina 3.125 g':
        searchmed = medicamento.replace('3.125 g', '').replace(' ', '%20')
    elif medicamento in ['penprocilina 400000', 'penprocilina 800000']:
        searchmed = medicamento.replace(' 400000', '').replace(' 800000', '').replace(' ', '%20')
    else:
        searchmed = medicamento.replace(' ', '%20')

    driver.get(command.replace('####', searchmed))
    assert "Chedraui" in driver.title

    try:
        wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, 'ol.breadcrumb')))
    except exceptions.TimeoutException:
        pass

    page = driver.execute_script("return document.documentElement.innerHTML;")
    driver.close()

    prod_list = []
    if '0 Artículos' not in page:
        prods = re.findall(p_prod, page)
        precs = re.findall(p_prec, page)[1::2]
        corr = 1
        if '10% Desc en toda' in page:
            corr = 0.9

        for name, price in zip(prods, precs):
            name = unidecode(name.replace('alt=', '').replace('"', '').lower())
            price = str(float(price.replace('$', '').replace('</div', '').replace(',', '')) * corr)
            submed = medicamento.replace('pediatrico', 'ped').replace('expectorante', 'expec').\
                replace('bencilpenicilina 800000', 'bencilpenicilina').replace('klaricid hp', 'klaricid h p').\
                replace('klaricid 12h', 'klaricid').replace('pedialyte 60 meq', 'pedialyte').\
                replace('pedialyte 45 meq', 'pedialyte').replace('infantil', 'inf').\
                replace('garamicina gu', 'garamicina g u').replace('junior', 'jr').\
                replace('posipen 12h', 'posipen 12 h').replace('reddy adulto', 'reddy').\
                replace('adulto', 'ad').replace('3.125 g', '').replace('ceftrex im', 'ceftrex i m').\
                replace('enzimatico', 'enz').replace('ovulo de 1 dia', '1 day ovule').\
                replace('merrem iv', 'merrem i v').replace('penprocilina 400000', 'penprocilina 400.000').\
                replace('vitapyrena', 'pyrena').replace('clasico', 'cla').split(' ')
            if all(x in name for x in submed):
                prod_list.append([name, price])
        if not prod_list:
            div = page.split('/* Add Product Data */')[-1].split('/* Set Action to PDP View */')[0]
            p_prod = "'name': '.*?'"
            p_prec = "'price' : '.*?'"
            try:
                prod = re.findall(p_prod, div)[0]
                prec = re.findall(p_prec, div)[0]
                f_prod = prod.replace("'name': ", "").replace("'", "")
                f_prec = str(float(prec.replace("'price' : ", "").replace("'", "").replace(",", "")) * corr)
                if len(f_prod) > 1 and len(f_prec) > 1:
                    prod_list.append([f_prod, f_prec])
            except IndexError:
                pass

    return prod_list
