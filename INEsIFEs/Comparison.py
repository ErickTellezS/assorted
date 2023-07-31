import FaceFunctions
import cv2
import datetime
from glob import glob
from os import makedirs, rename, remove
from os.path import join, exists, splitext, basename

base_path = join('/', 'home', 'erick', 'PycharmProjects', 'Base', 'INEsIFEs', 'FotosApp')
db_path = join(base_path, 'Caras')
photos_path = join(base_path, 'INEs')


def face_assign(pic_loc, thresh):
    database = FaceFunctions.setup_database(db_path)  # Create database

    if not exists(base_path + '/Reconocidos'):
        makedirs(base_path + '/Reconocidos')
    for filename in glob(join(pic_loc, '*.jpg')):
        photo = cv2.imread(filename)
        result, percentage = FaceFunctions.face_comparison(photo, database, thresh)
        identity = splitext(basename(filename))[0]
        if result is not None:
            file_path = base_path + '/Reconocidos' + '/' + identity.replace('_ID', '')
            if not exists(file_path):
                makedirs(file_path)
            rename(filename, file_path + '/' + identity + '.jpg')  # Move tested to recognized
            rename(join(db_path, result + '.jpg'), join(file_path, result + '.jpg'))  # Move from db to recognized
            print(identity, ' is ', result, ' with percentage: ', percentage)
    remove(db_path + '/faces_db.npy')  # Remove last db


starttime = datetime.datetime.now()

print('\nInitializing first part...')
face_assign(photos_path, 49)

print('\nInitializing second part...')
# Redo but less strict
face_assign(photos_path, 40)

stoptime = datetime.datetime.now()
print()
print('Started at ', starttime)
print('Ended at ', stoptime)
