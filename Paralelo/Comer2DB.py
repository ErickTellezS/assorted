import psycopg2
from unidecode import unidecode
from datetime import date
from BuscaComer import look_comer


def to_db(sub_id, sup_id, num_proc):
    connection = None
    cursor = None
    cursor2 = None
    to_base = None
    try:
        today = date.today().strftime("%d/%m/%Y")

        in_comer = []
        notin_comer = []

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
            to_fill = [id_, today] + [0 for x in range(4)]
            med = unidecode(medicamento[2].lower()).replace('.', '')
            n_c += 1
            print('Proceso: ', num_proc, 'Llevo', n_c)
            if med not in in_comer and med not in notin_comer:
                results = look_comer(med)
                if not results:
                    notin_comer.append(med)
                    to_fill[-1] = 2
                else:
                    in_comer.append(med)
                    num_prod = 0
                    num_prod_altern = 0
                    if pres != '':
                        p_list = []
                        p_list_altern = []
                        for prod in results:
                            name = prod[0]
                            desc = prod[1]
                            price = prod[2]

                            div_pres = pres.split(' ')
                            pres_in = False
                            nums_name = ''.join((ch if ch in '0123456789.' else ' ') for ch in name)
                            div_name = []
                            for i in nums_name.split():
                                try:
                                    div_name.append(float(i))
                                except ValueError:
                                    pass
                            nums_desc = ''.join((ch if ch in '0123456789.' else ' ') for ch in desc)
                            div_desc = []
                            for i in nums_desc.split():
                                try:
                                    div_desc.append(float(i))
                                except ValueError:
                                    pass
                            for div in div_pres:
                                try:
                                    if float(div) in div_name or float(div) in div_desc:
                                        pres_in = True
                                except ValueError:
                                    pass
                            if pres_in:
                                if frm != '':
                                    div_frm = frm.replace('/', ' ').replace(' ml', '').replace(' mg', '').replace(
                                        ' mcg',
                                        ''). \
                                        replace(' g', '').split(' ')
                                    isin = 0
                                    for div in div_frm:
                                        if div in name or div in desc:
                                            isin += 1
                                    if isin / len(div_frm) > 0.5:
                                        num_prod += 1
                                        p_list.append(float(price))
                                    else:
                                        num_prod_altern += 1
                                        p_list_altern.append(float(price))
                                else:
                                    num_prod += 1
                                    p_list.append(float(price))

                        if num_prod > 0:
                            to_fill[2] = num_prod
                            to_fill[3] = min(p_list)
                            to_fill[4] = max(p_list)
                        elif num_prod_altern > 0:  # Tipo 3
                            to_fill[2] = num_prod_altern
                            to_fill[3] = min(p_list_altern)
                            to_fill[4] = max(p_list_altern)
                    else:
                        p_list = []
                        for prod in results:
                            p_list.append(float(prod[2]))
                        num_prod = len(results)
                        to_fill[2] = num_prod
                        to_fill[3] = min(p_list)
                        to_fill[4] = max(p_list)

                    if num_prod != 0:
                        to_fill[-1] = 1
                    elif num_prod_altern != 0:
                        to_fill[-1] = 3
                    else:
                        to_fill[-1] = 2
            to_base.append(tuple(to_fill))
            medicamento = cursor.fetchone()
            if n_c % 100 == 0:
                for fill in to_base:
                    cursor2.execute("INSERT INTO la_comer VALUES {}".format(fill))
                connection.commit()
                to_base = []

    except (Exception, psycopg2.Error) as error:
        print('Error en proceso', num_proc)
        print(error)
    finally:
        if connection:
            for fill in to_base:
                cursor2.execute("INSERT INTO la_comer VALUES {}".format(fill))
            connection.commit()
            cursor.close()
            cursor2.close()
            connection.close()
