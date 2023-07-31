import re
from unidecode import unidecode
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.common import exceptions
from selenium.webdriver.chrome.options import Options as COptions


def look_rappi(medicamento):
    med_tree = {medicamento: {}}
    p_prec = 'p class="product-price"\\>.*?\\<'
    p_prod = 'p class="product-name"\\>.*?\\<'

    options = COptions()
    options.headless = True
    options.add_argument('--no-proxy-server')

    driver = webdriver.Chrome(executable_path='/home/erick/PycharmProjects/chromedriver', options=options)
    wait = WebDriverWait(driver, 600)

    searchmed = medicamento.replace(' ', '%20')
    command = "https://www.rappi.com.mx/search?store_type=all&query=####&search_type=TYPED"

    driver.get(command.replace('####', searchmed))
    assert "Rappi" in driver.title

    try:
        wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, 'div.search-option.active')))
    except exceptions.TimeoutException:
        pass

    wait = WebDriverWait(driver, 3)
    try:
        wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, 'p.title')))
    except exceptions.TimeoutException:
        pass
    page = driver.execute_script("return document.documentElement.innerHTML;")
    driver.close()

    if 'p class="title">' in page:
        sub_pages = page.split('p class="title">')
        for page in sub_pages[1:]:
            tienda = ''
            for ch in page:
                if ch != '<':
                    tienda += ch
                else:
                    break
            med_tree[medicamento][tienda] = []
            precios = re.findall(p_prec, page)
            productos = re.findall(p_prod, page)

            for n, p in zip(productos, precios):
                nombre = n.replace('p class="product-name">', '').replace('<', '')
                precio = p.replace('p class="product-price">', '').replace('<', '').replace(' ', '').replace('$', '')\
                    .replace(',', '')
                nombre = unidecode(nombre.lower())
                submed = medicamento.replace('pediatrico', 'pedi').split(' ')
                if nombre != '' and all(x in nombre for x in submed):
                    med_tree[medicamento][tienda].append([nombre, precio])
            if not med_tree[medicamento][tienda]:
                med_tree[medicamento].pop(tienda, None)
    return med_tree
