import cv2
from datetime import *
import requests
import time


data = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

webcam = cv2.VideoCapture(0)


def ping():

    nowtime = datetime.now()

    time = nowtime.strftime("%H:%M:%S")
    today = date.today()
    datenow = today.strftime("%d/%m/%Y")
    jsondata = {"value 1": datenow}
    requests.post(
        "https://maker.ifttt.com/trigger/IntruderAlert/with/key/cTf-Zbi3ngYw3Y5epFEW7z"
    )


while True:

    successful_frame_read, frame = webcam.read()
    greyscaleimg = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = data.detectMultiScale(greyscaleimg)
    try:
        if faces.any():

            ping()
            time.sleep(1800)

    except:
        pass

    key = cv2.waitKey(1)
