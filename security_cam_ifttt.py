#imports
import cv2
from datetime import datetime, timedelta, date
import requests
from dotenv import load_dotenv
import os
from imgurpython import ImgurClient
#initialist/load everything
load_dotenv()

client_id = os.getenv("ID")
client_secret = os.getenv("SECRET")
client = ImgurClient(client_id, client_secret)

load_dotenv()

data = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
webcam = cv2.VideoCapture(0)

last_ping_time = datetime.min  

#function when face is detected
def ping(frame, faces):
    global last_ping_time
    nowtime = datetime.now()
    time_str = nowtime.strftime("%H:%M:%S")
    today = date.today()
    datenow = today.strftime("%d/%m/%Y")

    # Draw rectangles around the faces
    for x, y, w, h in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

    # Save the frame as an image file
    path = f"intruder_{nowtime.strftime('%Y%m%d_%H%M%S')}.jpg"
    cv2.imwrite(path, frame)
    imageurl = (client.upload_from_path(path, config=None, anon=True))["link"]

    os.remove(path)
    #upload data
    jsondata = {"value1": datenow, "value2": imageurl}
    requests.post(
        "https://maker.ifttt.com/trigger/IntruderAlert/with/key/cTf-Zbi3ngYw3Y5epFEW7z",
        json=jsondata,
    )

    last_ping_time = nowtime  
    

#logic to handle face detection
while True:
    successful_frame_read, frame = webcam.read()
    greyscaleimg = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = data.detectMultiScale(greyscaleimg)

    current_time = datetime.now()
    if len(faces) > 0 and current_time - last_ping_time > timedelta(minutes=15):
        ping(frame, faces)

    key = cv2.waitKey(1)
    if key == ord("q"):
        break

# Release the webcam and close windows
webcam.release()
cv2.destroyAllWindows()
