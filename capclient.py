import os
import pickle
import subprocess
from time import time, sleep, asctime
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

SCR_DIR = "/sdcard/.tmp2"
FOLDER_ID = "place GDrive folder ID here"
SCOPES = ["https://www.googleapis.com/auth/drive"]


def backlight_on():
    with open("/sys/class/leds/lcd-backlight/brightness") as brightness:
        return int(brightness.read()) > 0


def gdrive_init():
    global service, is_gdrive_init
    if is_gdrive_init:
        return True
    try:
        service = build("drive", "v3", credentials=creds)
        is_gdrive_init = True
    except Exception:
        pass
    return is_gdrive_init


service = None
is_gdrive_init = False
# Place token.pickle initialized with SCOPE above in same dir as this program, GIYF
with open("token.pickle", "rb") as token:
    creds = pickle.load(token)
gdrive_init()

while True:
    date, hour = asctime()[4:10], asctime()[11:13]
    drc = os.path.join(SCR_DIR, date, hour)
    if backlight_on():
        if not os.path.exists(drc):
            os.makedirs(drc)
        pic_file = "%d.jpg" % time()
        pic_path = os.path.join(drc, pic_file)
        subprocess.call(
            ["minicap", "-P", "1080x1920@240x426/0", "-s"],
            stdout=open(pic_path, "w"),
            stderr=open(os.devnull, "w"),
        )
        # Upload to GDrive
        status = ""
        if gdrive_init():
            try:
                service.files().create(
                    body={"name": pic_file, "parents": [FOLDER_ID]},
                    media_body=MediaFileUpload(pic_path, mimetype="image/jpeg"),
                    fields="id",
                ).execute()
                status = "uploaded"
            except Exception:
                pass
        print pic_path[14:], status
    sleep(30)
