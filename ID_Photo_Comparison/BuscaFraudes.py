import psycopg2
import FaceFunctions
import cv2
from os.path import join

base_path = join('/', 'home', 'erick', 'PycharmProjects', 'Base', 'ID_Photo_Comparison')
faces_path = join(base_path, 'Caras')
ids_path = join(base_path, 'INEs')

cam = cv2.VideoCapture(0)
cv2.namedWindow("Photo Area")


def take_picture():
    in_type = None
    while True:
        ret, frame = cam.read()
        cv2.imshow("Photo Area", frame)
        if not ret:
            break
        k = cv2.waitKey(1)

        if k % 256 == 32:
            # F pressed
            in_type = 'pic'
            cv2.imwrite('temp.jpg', frame)
            break

    cam.release()
    cv2.destroyAllWindows()
    return in_type


def face_assign(filename, typefile, thresh):
    base_face = FaceFunctions.setup_database(faces_path)  # Create or load faces database
    base_id = FaceFunctions.setup_database(ids_path)  # Create or load ids database
    photo = cv2.imread(filename)
    result = None
    if typefile == 'id':
        result, percentage = FaceFunctions.face_comparison(photo, base_face, thresh)
    if typefile == 'pic':
        result, percentage = FaceFunctions.face_comparison(photo, base_id, thresh)
    if result is not None:
        return result
    else:
        return None


def check_db(filename, typefile, thresh):
    clue = face_assign(filename, typefile, thresh)
    tolook = None
    if typefile == 'id':
        tolook = 'id_foto'
    if typefile == 'pic':
        tolook = 'id_id'
    connection = None
    cursor = None
    try:
        connection = psycopg2.connect(user="postgres", password="0123456789", host="127.0.0.1", port="5432",
                                      database="Autos")
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM rentas WHERE TOLOOK = 'CLUE'".replace('TOLOOK', tolook).replace('CLUE', clue))
        data = cursor.fetchone()
        if data is None:
            cursor.execute("SELECT * FROM blacklist WHERE TOLOOK = 'CLUE'".replace('TOLOOK', tolook).
                           replace('CLUE', clue))
            data = cursor.fetchone()
        if connection:
            connection.commit()
            cursor.close()
            connection.close()
        return data

    except (Exception, psycopg2.Error):
        if connection:
            connection.commit()
            cursor.close()
            connection.close()
        return None


def veredict(db_data):
    if db_data is None:
        print('Esta persona no está en ninguna base de datos')
    elif len(db_data) == 6:
        print('Esta persona aparece como ' + ' '.join(db_data[2:5]) + ' y fue puesto en la lista negra en ' +
              db_data[5])
    else:
        if db_data[6]:
            print('Esta persona aparece como ' + ' '.join(db_data[2:5]) + ' y tiene una renta activa en ' + db_data[5])
        else:
            print('Esta persona aparece como ' + ' '.join(db_data[2:5]) + ' y realizó una devolución exitosa en ' +
                  db_data[5])


file = join(base_path, 'temp.jpg')
tipo = take_picture()
db_out = check_db(file, 'id', 49)
veredict(db_out)
