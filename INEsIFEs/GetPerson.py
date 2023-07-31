import FaceFunctions
import cv2
import datetime
from os import remove
from os.path import join, exists, splitext, basename
from PIL import Image


base_path = join('/', 'home', 'erick', 'PycharmProjects', 'Base', 'INEsIFEs', 'FotosApp')
db_path = join(base_path, 'Caras')
photos_path = join(base_path, 'INEs')


def face_assign(filename, thresh):
    database = FaceFunctions.setup_database(db_path)  # Create database
    photo = cv2.imread(filename)
    result, percentage = FaceFunctions.face_comparison(photo, database, thresh)
    identity = splitext(basename(filename))[0]
    if result is not None:
        print(identity, ' is ', result, ' with percentage: ', percentage)
        image = Image.open(join(db_path, result + '.jpg'))
        width, height = image.size
        if height > 600:
            fact = height/600
            width = int(width/fact)
            height = int(height/fact)

        image = image.resize((width, height))
        image.show()
    else:
        print('Try a better ID resolution')


starttime = datetime.datetime.now()

id_ = 'Fernanda_ID.jpg'
file = join(photos_path, id_)
face_assign(file, 50)

stoptime = datetime.datetime.now()
print()
print('Started at ', starttime)
print('Ended at ', stoptime)
