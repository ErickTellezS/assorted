import face_recognition
import cv2
import numpy as np
import glob
import os

face_cascade = cv2.CascadeClassifier('/home/erick/PycharmProjects/Base/haarcascades/'
                                     'haarcascade_frontalface_default.xml')


def get_face_embeddings_from_image(image, convert_to_rgb=False):
    """
    Take a raw image and run both the face detection and face embedding model on it
    """
    # Convert from BGR to RGB if needed
    if convert_to_rgb:
        image = image[:, :, ::-1]

    # run the face detection model to find face locations
    face_locations = face_recognition.face_locations(image)

    # run the embedding model to get face embeddings for the supplied locations
    face_encodings = face_recognition.face_encodings(image, face_locations)

    return face_locations, face_encodings


def setup_database(images_path, update=False):
    """
    Load reference images and create a database of their face encodings or opens an existing database
    """
    try:
        numofphotos, database = np.load(images_path + '/faces_db.npy')
        if update:
            changed = False
            for filename in glob.glob(os.path.join(images_path, '*.jpg')):
                # use the name in the filename as the identity key
                identity = os.path.splitext(os.path.basename(filename))[0]
                if identity not in database:
                    numofphotos += 1
                    image_rgb = face_recognition.load_image_file(filename)
                    locations, encodings = get_face_embeddings_from_image(image_rgb)
                    database[identity] = encodings[0]
                    changed = True
            if changed:
                np.save(images_path + '/faces_db', [numofphotos, database])
                print('Faces database updated and loaded.\n')
            else:
                print('Faces database loaded. No need to update it.\n')
        else:
            print('Faces database loaded.\n')

    except FileNotFoundError:
        database = {}
        numofphotos = 0
        for filename in glob.glob(os.path.join(images_path, '*.jpg')):
            # load image
            numofphotos += 1
            image_rgb = face_recognition.load_image_file(filename)

            # use the name in the filename as the identity key
            identity = os.path.splitext(os.path.basename(filename))[0]

            # get the face encoding and link it to the identity
            locations, encodings = get_face_embeddings_from_image(image_rgb)
            database[identity] = encodings[0]

        np.save(images_path + '/faces_db', [numofphotos, database])
        print('Faces database created and loaded.\n')

    return database


def face_comparison(photo2check, database, percentage_of_similarity):
    gray = cv2.cvtColor(photo2check, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    name = None
    best = None
    if len(faces) != 0:
        face_locations, face_encodings = get_face_embeddings_from_image(photo2check, convert_to_rgb=True)

        # the face_recognition library uses keys and values of your database separately
        known_face_encodings = list(database.values())
        known_face_names = list(database.keys())

        # Loop through each face in this frame of video and see if there's a match
        for location, face_encoding in zip(face_locations, face_encodings):

            # get the distances from this encoding to those of all reference images
            distances = face_recognition.face_distance(known_face_encodings, face_encoding)

            # select the closest match (smallest distance) if it's below the threshold value
            max_distance = 1 - (percentage_of_similarity / 100)
            if np.any(distances <= max_distance):
                best_match_idx = int(np.argmin(distances))
                name = known_face_names[best_match_idx]
                best = (1 - distances[best_match_idx]) * 100

    return name, best
