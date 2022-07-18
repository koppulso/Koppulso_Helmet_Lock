import cv2
from datetime import datetime
import os
import shutil


now = datetime.now()
year = now.strftime("%Y")
month = now.strftime("%m")
day = now.strftime("%d")
time = now.strftime("%H_%M_%S")

webcam = cv2.VideoCapture(1)


def get_dir_size(path='.'):
    total = 0
    with os.scandir(path) as it:
        for entry in it:
            if entry.is_file():
                total += entry.stat().st_size
            elif entry.is_dir():
                total += get_dir_size(entry.path)
    return total


def blackbox_play():
    if not webcam.isOpened():
        print("Could not open webcam")
        exit()

    os.makedirs('D:/%s/%s/%s' % (year, month, day), exist_ok=True)
    BB_Dir = 'D:/%s/%s/%s/%s.avi' % (year, month, day, time)

    fourcc = cv2.VideoWriter_fourcc(*'DIVX')
    out = cv2.VideoWriter(BB_Dir, fourcc, 25.0, (640, 480))

    if get_dir_size('D:/') > 13958643712:
        for x in range(1, 31):
            try:
                shutil.rmtree('D:/%s/%s/%s' % (year, month, str(int(day)-x).zfill(2)))
            except FileNotFoundError:
                pass

    while webcam.isOpened():
        status, frame = webcam.read()

        if not status:
            print("Could not read frame")
            exit()

        cv2.imshow("frame", frame)
        out.write(frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


webcam.release(blackbox_play())
cv2.destroyAllWindows()



