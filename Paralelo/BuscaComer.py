import re
from unidecode import unidecode
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.common import exceptions
from selenium.webdriver.chrome.options import Options as COptions


def look_comer(medicamento):
    p_prod = 'class="ng-binding"\\>.*?\\</strong'
    p_desc = 'p itemprop="description" class="ng-binding"\\>.*?\\</p'
    p_prec = 'span class="precio_old ng-binding"\\>.*?\\<'

    options = COptions()
    options.headless = True
    options.add_argument('--no-proxy-server')

    driver = webdriver.Chrome(executable_path='/home/erick/PycharmProjects/chromedriver', options=options)
    wait = WebDriverWait(driver, 600)

    criterio = medicamento.replace(' ', '+')
    final = medicamento.replace(' ', '%20')
    command = "https://www.lacomer.com.mx/lacomer/goBusqueda.action?succId=287&ver=mislistas&succFmt=100&criterio=" \
              "CRITERIO#/FINAL"

    driver.get(command.replace('CRITERIO', criterio).replace('FINAL', final))
    assert "La Comer" in driver.title

    try:
        wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, 'div.pb-5.cont_filtro_mp')))
    except exceptions.TimeoutException:
        pass

    page = driver.execute_script("return document.documentElement.innerHTML;")
    driver.close()

    prod_list = []
    if 'no_result_busqueda' not in page:
        prods = re.findall(p_prod, page)
        descs = re.findall(p_desc, page.replace('\n', ' '))
        precs = re.findall(p_prec, page)

        for name, desc, price in zip(prods, descs, precs):
            name = unidecode(name.replace('class="ng-binding">', '').replace('</strong', '').lower())
            desc = unidecode(desc.replace('p itemprop="description" class="ng-binding">', '').replace('</p', '').
                             replace('<br>', '').replace('\t', '').replace('&nbsp;', '').lower())
            price = price.replace('span class="precio_old ng-binding"> $', '').replace(' M.N. <', '').replace(',', '')

            submed = medicamento.replace('pediatrico', 'pedi').split(' ')
            if all(x in name for x in submed):
                prod_list.append([name, desc, price])
    return prod_list
