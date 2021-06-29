import numpy as np
import cv2

import time
import os

faceCascade = cv2.CascadeClassifier('haarcascades/haarcascade_frontalface_default.xml')
smileCascade = cv2.CascadeClassifier('haarcascades/haarcascade_eye.xml')
cap = cv2.VideoCapture(0)
cap.set(3, 640)  # set Width
cap.set(4, 480)  # set Height
count = 0
id_img = 0
while True:

    ret, img = cap.read()
    #img = cv2.flip(img, -1)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.2,
        minNeighbors=10,
        minSize=(20, 20),

    )
    if len(faces):
        print("found")
        count = 0

    else:
        print("not found")
        count += 1
    print(count)
    if count == 5:
        pass
        #os.system("Rundll32.exe user32.dll,LockWorkStation")


    for (x, y, w, h) in faces:
        id_img += 1
        cv2.imwrite(r"dataset\User.1" + '.' + str(id_img) + ".jpg", gray[y:y + h, x:x + w])

    #   cv2.rectangle(img, (x, y), (x + w, y + h), (125, 0, 0), 2)
    #    roi_gray = gray[y:y + h, x:x + w]
    #    roi_color = img[y:y + h, x:x + w]
    #cv2.destroyAllWindows()
    cv2.imshow('video', img)

    k = cv2.waitKey(30) & 0xff
    if k == 27:  # press 'ESC' to quit
        break
    elif id_img >= 60:
        break
    time.sleep(1)
cap.release()

