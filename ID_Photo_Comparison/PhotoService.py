import psycopg2
import FaceFunctions
import cv2
from os.path import join

base_path = join('/', 'home', 'erick', 'PycharmProjects', 'Base', 'ID_Photo_Comparison')
faces_path = join(base_path, 'Caras')
ids_path = join(base_path, 'INEs')


def get_person(file, *others):
    person = False
    id_, name, lst1, lst2 = None, None, None, None
    if len(list(others)) == 3:
        database = FaceFunctions.setup_database(faces_path)  # Create or load ids database
        name = others[0]
        lst1 = others[1]
        lst2 = others[2]
        person = True
    else:
        database = FaceFunctions.setup_database(ids_path)  # Create or load faces database
        id_ = others[0]

    photo = cv2.imread(file)
    result, percentage = FaceFunctions.face_comparison(photo, database, 49)
    photo_id = str(result)
    connection = psycopg2.connect(user="postgres", password="0123456789", host="127.0.0.1", port="5432",
                                  database="Autos")
    cursor = connection.cursor()
    if person:
        cursor.execute("SELECT * FROM(SELECT * FROM rentas UNION SELECT *, NULL FROM blacklist) "
                       "AS mini WHERE id_foto = 'CLUE'".replace('CLUE', photo_id))
        data = cursor.fetchone()
        if data:
            id_ = result
            if data[-1]:
                status = 'A'
            elif data[-1] is None:
                status = 'B'
            else:
                status = 'I'
        else:
            id_ = '00000000'
            status = 'N'
        cursor.execute("INSERT INTO processing VALUES " + "('" + "', '".join([id_, name, lst1, lst2, status]) + "')")
        connection.commit()
        cursor.close()
        connection.close()
        return id_
    else:
        cursor.execute("SELECT * FROM processing WHERE id_foto = '###'".replace('###', id_))
        data = cursor.fetchone()
        id_ = data[0]
        rep_name = ' '.join([data[1], data[2], data[3]])
        status = data[4]
        cursor.execute("DELETE FROM processing WHERE id_foto = '###'".replace('###', id_))
        connection.commit()

        cursor.execute("SELECT * FROM(SELECT * FROM rentas UNION SELECT *, NULL FROM blacklist) "
                       "AS mini WHERE id_id = '###'".replace('###', str(result)))
        db_name = None
        data = cursor.fetchone()
        if data is not None:
            checkid = data[1]
            db_name = ' '.join([data[2], data[3], data[4]])
        else:
            checkid = id_
        cursor.close()
        connection.close()
        msg = None
        if (id_ == '00000000' and result is not None) or (result is None and id_ != '00000000') or id_ != checkid:
            msg = 'La foto en la credencial no corresponde con la persona.'
        else:
            if id_ != '00000000':
                if db_name != rep_name:
                    msg = 'Esta persona está en la base de datos con un nombre diferente al que reporta.'
                else:
                    if status == 'A':
                        msg = 'Esta persona tiene un renta activa en ###.'. replace('###', data[5])
                    if status == 'I':
                        msg = 'Esta persona regresó exitosamente su auto en ###.'. replace('###', data[5])
                    if status == 'B':
                        msg = 'Esta persona fue puesta en la lista negra en ###.'. replace('###', data[5])
            else:
                msg = 'Esta persona es nueva en el sistema.'
        return msg


foto = join(base_path, 'Personas', 'ahide.jpg')
id_id = get_person(foto, 'AHIDE', 'BAUTISTA', 'HERNANDEZ')
print(id_id)

identificacion = join(base_path, 'INEs2Check', 'ahide_id.jpg')
print(get_person(identificacion, id_id))
