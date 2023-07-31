import Classifier
import cv2
import numpy as np
import csv

photo = '1'
img1 = cv2.imread('/home/erick/PycharmProjects/Base/INEsIFEs/FotosApp/photo' + photo + '.jpg')
facelines1, gender1, age1, vect1 = Classifier.get_face(img1)

for x in range(1, 19):
    img2 = cv2.imread('/home/erick/PycharmProjects/Base/INEsIFEs/FotosApp/photo' + str(x) + '.jpg')
    facelines2, gender2, age2, vect2 = Classifier.get_face(img2)
    print('photo' + photo + '.jpg vs photo' + str(x) + '.jpg')
    print('Diferencia: ', sum(abs(vect1 - vect2)))
    print(list(abs(vect1 - vect2)))
    print()

#cv2.imshow('Face', facelines1)
#cv2.waitKey()

'''with open('CompChecker.csv', mode='w') as checker:
    checker_writer = csv.writer(checker, delimiter=';')
    checker_writer.writerow([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18])
    for x in range(1, 19):
        print('photo' + str(x) + '.jpg vs:')
        towrite = [x]
        img1 = cv2.imread('/home/erick/PycharmProjects/Base/INEsIFEs/FotosApp/photo' + str(x) + '.jpg')
        facelines1, gender1, age1, vect1 = Classifier.get_face(img1)
        for y in range(1, 19):
            print('\t photo' + str(y) + '.jpg')
            if x == y:
                towrite.append('M')
            else:
                img2 = cv2.imread('/home/erick/PycharmProjects/Base/INEsIFEs/FotosApp/photo' + str(y) + '.jpg')
                facelines2, gender2, age2, vect2 = Classifier.get_face(img2)
                dif = sum(abs(vect1 - vect2))
                if dif < 0.5:
                    towrite.append('O')
                else:
                    towrite.append('X')
        checker_writer.writerow(towrite)'''

#for x in range(1, 19):
 #   img = cv2.imread('/home/erick/PycharmProjects/Base/INEsIFEs/FotosApp/photo' + str(x) + '.jpg')
  #  facelines, gender, age, vect = Classifier.get_face(img)
  #  print('photo' + str(x) + '.jpg')
   # print('Max: ', list(vect).index(1))
   # print()
