import cv2
import win32event
import win32serviceutil
import win32service
import servicemanager
import sys
import os
import time
import winreg as reg
import logging

class Lock(win32serviceutil.ServiceFramework):
    _svc_name_ = 'LockLA'
    _svc_display_name_ = 'LockLA'
    _svc_description_ = 'Lock Lazy Admin'

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        self.isAlive = True
        with reg.OpenKey(reg.HKEY_LOCAL_MACHINE, "SYSTEM\\CurrentControlSet\\Services\\LockLA") as h:
           self.path = reg.EnumValue(h, 3)[1].strip("lock_la.exe")
        #self.path = r"D:\myApp\LoginLA\\"
        logging.basicConfig(
            level=logging.INFO,
            filename=self.path + "lock.log",
            format='[AgentLA] %(asctime)s %(levelname)s %(message)s')

    def main(self):
        faceCascade = cv2.CascadeClassifier(self.path + 'haarcascades/haarcascade_frontalface_default.xml')
        cap = cv2.VideoCapture(0)
        cap.set(3, 640)
        cap.set(4, 480)
        count = 0


        while self.isAlive:
            ret, img = cap.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = faceCascade.detectMultiScale(
                gray,
                scaleFactor=1.2,
                minNeighbors=5,
                minSize=(20, 20),
            )
            if len(faces):
                logging.info("found")
                count = 0

            else:
                logging.info("not found")
                count += 1
            print(count)
            if count == 5:
                pass
                os.system('rundll32.exe user32.dll, LockWorkStation')
            #for (x, y, w, h) in faces:
                #id_img += 1
                #cv2.imwrite(r"dataset\User.1" + '.' + str(id_img) + ".jpg", gray[y:y + h, x:x + w])

            #   cv2.rectangle(img, (x, y), (x + w, y + h), (125, 0, 0), 2)
            #    roi_gray = gray[y:y + h, x:x + w]
            #    roi_color = img[y:y + h, x:x + w]
            #cv2.destroyAllWindows()
            #cv2.imshow('video', img)

            k = cv2.waitKey(30) & 0xff
            #if k == 27:  # press 'ESC' to quit
            #    break
            #elif id_img >= 60:
            #    break
            time.sleep(1)

        cap.release()

    def SvcDoRun(self):
        self.isAlive = True
        self.ReportServiceStatus(win32service.SERVICE_START_PENDING)
        self.ReportServiceStatus(win32service.SERVICE_RUNNING)
        self.main()
        win32event.WaitForSingleObject(self.hWaitStop, win32event.INFINITE)

    def SvcStop(self):
        self.isAlive = False
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)


if __name__ == '__main__':
    if len(sys.argv) == 1:
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(Lock)
        servicemanager.StartServiceCtrlDispatcher()
    else:
        win32serviceutil.HandleCommandLine(Lock)



