import psycopg2
from unidecode import unidecode
from datetime import date
from BuscaRappi import look_rappi


def to_db(sub_id, sup_id, num_proc):
    connection = None
    cursor = None
    cursor2 = None
    to_base = None
    try:
        today = date.today().strftime("%d/%m/%Y")

        stores = ['del ahorro', 'san pablo', 'guadalajara', 'benavides', 'similares', 'la comer', 'chedraui', 'costco',
                  'sumesa', 'superama', 'soriana', 'city market', 'sanborns']
        in_rappi = []
        notin_rappi = []
        inserted = []

        connection = psycopg2.connect(user="postgres", password="0123456789", host="127.0.0.1", port="5432",
                                      database="Farmacias")
        cursor = connection.cursor()
        cursor2 = connection.cursor()
        cursor.execute("SELECT * FROM med_base WHERE id >= {} AND id <= {}".format(sub_id, sup_id))

        medicamento = cursor.fetchone()
        n_c = 0
        to_base = []
        while medicamento:
            id_ = medicamento[0]
            pres = unidecode(medicamento[3].lower())
            frm = unidecode(medicamento[4].lower())
            to_fill = [id_, today] + [0 for x in range(40)]
            med = unidecode(medicamento[2].lower()).replace('.', '')
            n_c += 1
            print('Proceso: ', num_proc, 'Llevo', n_c)
            if med not in in_rappi and med not in notin_rappi:
                results = look_rappi(med)
                if results[med] == {}:
                    notin_rappi.append(med)
                    to_fill[-1] = 2
                else:
                    in_rappi.append(med)
                    num_prod = 0
                    num_prod_altern = 0
                    for tienda in results:
                        for store in stores:
                            if store in tienda.lower():
                                ind_s = (stores.index(store) * 3) + 2
                                ind_m = ind_s + 1
                                ind_M = ind_m + 1
                                if pres != '':
                                    num_prod = 0
                                    p_list = []
                                    num_prod_altern = 0
                                    p_list_altern = []
                                    for prod in results[tienda]:
                                        name = prod[0]
                                        price = prod[1]
                                        if frm != '':
                                            div_frm = frm.replace('/', ' ').replace(' ml', '').replace(' mg', ''). \
                                                replace(' mcg', '').replace(' g', '').split(' ')
                                            comp = [pres] + div_frm
                                        else:
                                            comp = [pres]
                                        isin = 0
                                        for div in comp:
                                            if div in name:
                                                isin += 1
                                        if isin / len(comp) > 0.5:
                                            num_prod += 1
                                            p_list.append(float(price))
                                        else:
                                            num_prod_altern += 1
                                            p_list_altern.append(float(price))
                                    if num_prod > 0:
                                        to_fill[ind_s] = num_prod
                                        to_fill[ind_m] = min(p_list)
                                        to_fill[ind_M] = max(p_list)

                                    elif num_prod_altern > 0:  # Tipo 3
                                        to_fill[ind_s] = num_prod_altern
                                        to_fill[ind_m] = min(p_list_altern)
                                        to_fill[ind_M] = max(p_list_altern)

                                else:
                                    prods = results[tienda]
                                    num_prod = len(prods)
                                    if num_prod == 1:
                                        price = prods[0][1]
                                        to_fill[ind_s] = 1
                                        to_fill[ind_m] = float(price)
                                        to_fill[ind_M] = float(price)
                                    else:
                                        p_list = []
                                        to_fill[ind_s] = num_prod
                                        for prod in prods:
                                            p_list.append(float(prod[1]))
                                        to_fill[ind_m] = min(p_list)
                                        to_fill[ind_M] = max(p_list)
                    if num_prod != 0:
                        to_fill[-1] = 1
                    elif num_prod_altern != 0:
                        to_fill[-1] = 3
                    else:
                        to_fill[-1] = 2
                    inserted.append(id_)
            to_base.append(tuple(to_fill))
            medicamento = cursor.fetchone()
            if n_c % 100 == 0:
                for fill in to_base:
                    cursor2.execute("INSERT INTO rappi VALUES {}".format(fill))
                connection.commit()
                to_base = []

    except (Exception, psycopg2.Error) as error:
        print('Error en proceso', num_proc)
        print(error)
    finally:
        if connection:
            for fill in to_base:
                cursor2.execute("INSERT INTO rappi VALUES {}".format(fill))
            connection.commit()
            cursor.close()
            cursor2.close()
            connection.close()
