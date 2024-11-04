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


data = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
webcam = cv2.VideoCapture(0)

last_ping_time = datetime.min  # Initialize to a very old date

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
    url = "https://api.brevo.com/v3/smtp/email"

    payload = {
        "sender": {"name": "Security Cam", "email": "paddydevacc@gmail.com"},
        "to": [{"email": "onslowpaddy@gmail.com", "name": "Paddy Cooper"}],
        "subject": "Intruder Alert",
        "htmlContent": f"""
    <html>
        <body>
            <h1>Intruder Alert</h1>
            <p>Intruder detected on {datenow} at {time_str}</p>
            <img src="{imageurl}" alt="Intruder Image" />
        </body>
    </html>
    """,
    }
    headers = {
        "content-type": "application/json",
        "accept": "application/json",
        "api-key": os.getenv("KEY"),
    }

    response = requests.post(url, json=payload, headers=headers)

    print(response.json())

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


# Release the webcam and close windows
webcam.release()
cv2.destroyAllWindows()
