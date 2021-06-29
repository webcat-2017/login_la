import cv2
import numpy as np
import os
import time
from winreg import *
import pyautogui


recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('trainer/trainer.yml')
cascadePath = "haarcascades/haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath)

font = cv2.FONT_HERSHEY_SIMPLEX

# iniciate id counter
id = 0

# names related to ids: example ==> Marcelo: id=1,  etc
names = ['None', 'Lazy Admin', 'Paula', 'Ilza', 'Z', 'W']

# Initialize and start realtime video capture
cam = cv2.VideoCapture(0)
cam.set(3, 640)  # set video widht
cam.set(4, 480)  # set video height

# Define min window size to be recognized as a face
minW = 0.1 * cam.get(3)
minH = 0.1 * cam.get(4)
count = 0
while True:

    ret, img = cam.read()
    #img = cv2.flip(img, -1)  # Flip vertically

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.2,
        minNeighbors=10,
        minSize=(int(minW), int(minH)),
    )

    for (x, y, w, h) in faces:

        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

        id, confidence = recognizer.predict(gray[y:y + h, x:x + w])

        # Check if confidence is less them 100 ==> "0" is perfect match
        if (confidence < 100):
            id = names[id]
            confidence = "  {0}%".format(round(100 - confidence))
        else:
            id = "ENEMY!!!!"
            confidence = "  {0}%".format(round(100 - confidence))
        if int(confidence.replace("%", "")) >= 50:
            print("Login")
            os.system("explorer")

            #key = OpenKey(HKEY_LOCAL_MACHINE, 'SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon', 0,
             #             KEY_ALL_ACCESS)
            #SetValueEx(key, "DefaultUserName", 0, REG_SZ, "Vlasyuk")
            #SetValueEx(key, "DefaultPassword", 0, REG_SZ, "Rt200744q")
            #SetValueEx(key, "AutoAdminLogon", 0, REG_DWORD, 1)
            #CloseKey(key)

        cv2.putText(img, str(id,), (x + 5, y - 5), font, 1, (255, 255, 255), 2)
        cv2.putText(img, str(confidence), (x + 5, y + h - 5), font, 1, (255, 255, 0), 1)

    cv2.imshow('camera', img)

    if len(faces):
        print("found")
        count = 0

    else:
        print("not found")
        count += 1
    print(count)
    if count == 5:
        pass
        os.system("Rundll32.exe user32.dll,LockWorkStation")


    k = cv2.waitKey(10) & 0xff  # Press 'ESC' for exiting video
    if k == 27:
        break

    time.sleep(1)

# Do a bit of cleanup
print("\n [INFO] Exiting Program and cleanup stuff")
cam.release()
cv2.destroyAllWindows()
