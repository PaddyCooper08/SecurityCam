import cv2
from datetime import *
import yagmail
import time
from dotenv import load_dotenv
import os
load_dotenv()
env_path = Path('.')/'.env'
load_dotenv(dotenv_path=env_path)
yagmail.register(os.getenv("USER"), os.getenv("PASSWORD"))


data = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

webcam = cv2.VideoCapture(0)


def ping():

    nowtime = datetime.now()

    time = nowtime.strftime("%H:%M:%S")
    today = date.today()
    datenow = today.strftime("%d/%m/%Y")

    yag = yagmail.SMTP("PaddyDevAcc@gmail.com")
    yag.send(
        to="1210@rgsg.co.uk",
        contents=f"Security camera triggered at {time} on the {datenow}",
        subject="Security alert",
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
