# import the necessary packages
from imutils import face_utils
import numpy as np
from math import sqrt
import imutils
import dlib
import cv2

# initialize dlib's face detector (HOG-based) and then create
# the facial landmark predictor
detector = dlib.get_frontal_face_detector()

predictor = dlib.shape_predictor('/home/erick/PycharmProjects/Base/INEsIFEs/FotosApp/'
                                 'shape_predictor_68_face_landmarks.dat')

# load the input image, resize it, and convert it to grayscale


def get_face(image):
    # image = imutils.resize(image, width=500)
    justmarks = []
    gender = None
    age = None
    distanceslist = None
    blank = np.zeros(image.shape)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    model_mean_values = (78.4263377603, 87.7689143744, 114.895847746)
    age_list = ['(0, 2)', '(4, 6)', '(8, 12)', '(15, 20)', '(25, 32)', '(38, 43)', '(48, 53)', '(60, 100)']
    gender_list = ['Male', 'Female']

    # detect faces in the grayscale image
    rects = detector(gray, 1)

    age_net = cv2.dnn.readNetFromCaffe("age_gender_models/deploy_age.prototxt", "age_gender_models/age_net.caffemodel")
    gender_net = cv2.dnn.readNetFromCaffe("age_gender_models/deploy_gender.prototxt",
                                          "age_gender_models/gender_net.caffemodel")

    # loop over the face detections
    for (i, rect) in enumerate(rects):
        # determine the facial landmarks for the face region, then
        # convert the facial landmark (x, y)-coordinates to a NumPy
        # array
        shape = face_utils.shape_to_np(predictor(gray, rect))

        # convert dlib's rectangle to a OpenCV-style bounding box
        # [i.e., (x, y, w, h)], then draw the face bounding box
        (x, y, w, h) = face_utils.rect_to_bb(rect)
        face = image[y:y + h, x:x + w].copy()

        blob = cv2.dnn.blobFromImage(face, 1, (227, 227), model_mean_values, swapRB=False)

        # Predict gender
        gender_net.setInput(blob)
        gender_preds = gender_net.forward()
        gender = gender_list[gender_preds[0].argmax()]
        # Predict age
        age_net.setInput(blob)
        age_preds = age_net.forward()
        age = age_list[age_preds[0].argmax()]

        # parts of face
        '''chin = [tuple(shape[1]), tuple(shape[4]), tuple(shape[8]), tuple(shape[12]), tuple(shape[15])]
        reyebrow = [tuple(shape[17]), tuple(shape[21])]
        leyebrow = [tuple(shape[22]), tuple(shape[26])]
        nose = [tuple(shape[27]), tuple(shape[31]), tuple(shape[33]), tuple(shape[35])]
        reye = [tuple(shape[36]), tuple(shape[39])]
        leye = [tuple(shape[42]), tuple(shape[45])]
        mouth = [tuple(shape[48]), tuple(shape[54])]

        mostleft = chin[0][0] - 10
        mostright = chin[4][0] + 10
        mostup = min(reyebrow[0][1], leyebrow[0][1], reyebrow[1][1], leyebrow[1][1]) - 10
        mostdown = chin[2][1] + 10

        face = chin + reyebrow + leyebrow + nose + reye + leye + mouth

        distances = []
        for tuples in range(len(face)):
            cv2.circle(blank, (face[tuples][0], face[tuples][1]), 1, (255, 0, 0), 3)
            x2 = face[0][0]
            x1 = face[tuples][0]
            y2 = face[0][1]
            y1 = face[tuples][1]
            if tuples + 1 < len(face):
                x2 = face[tuples + 1][0]
                y2 = face[tuples + 1][1]

            # cv2.line(blank, (x1, y1), (x2, y2), (0, 0, 255), 3)
            d = sqrt(((x2 - x1) ** 2) + ((y2 - y1) ** 2))
            distances.append(d)
        distanceslist = np.array(distances) / max(distances)

        # draw chin lines
        cv2.line(blank, chin[0], chin[1], (0, 255, 0), 1)
        cv2.line(blank, chin[1], chin[2], (0, 255, 0), 1)
        cv2.line(blank, chin[2], chin[3], (0, 255, 0), 1)
        cv2.line(blank, chin[3], chin[4], (0, 255, 0), 1)

        # draw eyebrows lines
        cv2.line(blank, reyebrow[0], reyebrow[1], (0, 255, 0), 1)
        cv2.line(blank, leyebrow[0], leyebrow[1], (0, 255, 0), 1)

        # draw nose lines
        cv2.line(blank, nose[0], nose[2], (0, 255, 0), 1)
        cv2.line(blank, nose[1], nose[2], (0, 255, 0), 1)
        cv2.line(blank, nose[2], nose[3], (0, 255, 0), 1)

        # draw eyes lines
        cv2.line(blank, reye[0], reye[1], (0, 255, 0), 1)
        cv2.line(blank, leye[0], leye[1], (0, 255, 0), 1)

        # draw mouth line
        cv2.line(blank, mouth[0], mouth[1], (0, 255, 0), 1)

        justmarks = blank[mostup:mostdown, mostleft:mostright]'''

        chin = [tuple(shape[0]), tuple(shape[8]), tuple(shape[16])]
        nosebone = [tuple(shape[27]), tuple(shape[30])]
        reye = [tuple(shape[36]), tuple(shape[39])]
        leye = [tuple(shape[42]), tuple(shape[45])]

        philtrum = [tuple(shape[30]), tuple(shape[33])]
        bridge = [tuple(shape[39]), tuple(shape[42])]
        reargap = [tuple(shape[0]), tuple(shape[36])]
        leargap = [tuple(shape[16]), tuple(shape[45])]
        cross = [tuple(shape[8]), tuple(shape[27])]
        reyechin = [tuple(shape[8]), tuple(shape[36])]
        leyechin = [tuple(shape[8]), tuple(shape[45])]
        ear2ear = [tuple(shape[0]), tuple(shape[16])]
        reyep = [tuple(shape[33]), tuple(shape[39])]
        leyep = [tuple(shape[33]), tuple(shape[42])]

        face = [chin, nosebone, reye, leye]

        gaps = [philtrum, bridge, reargap, leargap, cross, reyechin, leyechin, ear2ear, reyep, leyep]

        distances = []
        for part in face + gaps:
            for tuples in range(len(part) - 1):
                cv2.circle(blank, (part[tuples][0], part[tuples][1]), 1, (255, 0, 0), 3)
                cv2.circle(blank, (part[tuples + 1][0], part[tuples + 1][1]), 1, (255, 0, 0), 3)
                x2 = part[tuples + 1][0]
                x1 = part[tuples][0]
                y2 = part[tuples + 1][1]
                y1 = part[tuples][1]
                if part in face:
                    cv2.line(blank, (x1, y1), (x2, y2), (0, 255, 0), 1)
                else:
                    cv2.line(blank, (x1, y1), (x2, y2), (0, 0, 255), 1)
                d = sqrt(((x2 - x1) ** 2) + ((y2 - y1) ** 2))
                distances.append(d)
        distances[12] = distances[12] * 2
        distanceslist = np.array(distances) / max(distances)

        mostup = min([shape[19][1], shape[24][1]]) - 10
        mostdown = shape[8][1] + 10
        mostright = shape[16][0] + 10
        mostleft = shape[0][0] - 10
        justmarks = blank[mostup:mostdown, mostleft:mostright]

    return justmarks, gender, age, distanceslist


# show the output image with the face detections + facial landmarks
img = cv2.imread('/home/erick/PycharmProjects/Base/INEsIFEs/FotosApp/Caras/Ara.jpg')
#img = cv2.imread('/home/erick/PycharmProjects/Base/INEsIFEs/test')
facelines, gen, ag, vect = get_face(img)
print(vect)
cv2.imshow("Blank", facelines)
cv2.waitKey()
