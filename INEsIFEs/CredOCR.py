import cv2
import pytesseract

face_cascade = cv2.CascadeClassifier('/home/erick/PycharmProjects/Base/haarcascades/'
                                     'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('/home/erick/PycharmProjects/Base/haarcascades/haarcascade_eye.xml')
IDcard = cv2.imread('/home/erick/PycharmProjects/Base/INEsIFEs/FotosApp/INEs_Original/Antonio_ID.jpg')
gray = cv2.cvtColor(IDcard, cv2.COLOR_BGR2GRAY)
bw = None
faces = face_cascade.detectMultiScale(gray, 1.3, 5)
for (x, y, w, h) in faces:
    roi_gray = gray[y:y + h, x:x + w]
    roi_color = IDcard[y:y + h, x:x + w]
    eyes = eye_cascade.detectMultiScale(roi_gray)
    if len(eyes) != 0:
        roi_letters = gray[y:y + h, x + int(1.2 * w):x + 2 * w]
        (thresh, im_bw) = cv2.threshold(roi_letters, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        gray = gray[:, x + w:]
        bw = cv2.threshold(gray, thresh + 2, 255, cv2.THRESH_BINARY)[1]

partofname = 0
partofdir = 0
pile = ''
fathers = ''
mothers = ''
calle = ''
colonia = ''
alcaldia = ''
out = pytesseract.image_to_string(bw)
parsed = out.replace('  ', '').split('\n')
parsed = list(filter(None, parsed))
for line in parsed:
    print(line)
    if partofname == 3:
        for letter in line:
            if letter.isupper() or letter == ' ':
                pile = pile + letter
        if pile[-1] == ' ':
            pile = pile[:-1]
        partofname = 0
    if partofname == 2:
        spacecounter = 0
        for letter in line:
            if letter == ' ':
                spacecounter += 1
            if spacecounter == 2:
                break
            if letter.isupper() or letter == ' ':
                mothers = mothers + letter
        if mothers[-1] == ' ':
            mothers = mothers[:-1]
        partofname += 1
    if partofname == 1:
        for letter in line:
            if letter.isupper() or letter == ' ':
                fathers = fathers + letter
        if fathers[-1] == ' ':
            fathers = fathers[:-1]
        partofname += 1

    if partofdir == 3:
        alcaldia = line
        partofdir = 0
    if partofdir == 2:
        colonia = line
        partofdir += 1
    if partofdir == 1:
        if line[:3] != 'COL':
            calle = line
            partofdir += 1
        else:
            calle = 'N/A'
            colonia = line
            partofdir = 3

    if 'DOM' in line:
        partofdir = 1
    if 'NOM' in line:
        partofname = 1

print()
print(fathers)
print(mothers)
print(pile)
print()
print(calle)
print(colonia)
print(alcaldia)

# cv2.imshow('BW', bw)
# cv2.waitKey()
# cv2.destroyAllWindows()
