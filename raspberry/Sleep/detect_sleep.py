# リアルタイムで実装するならこっち（20fps出たわ）
# 1分間に11.5%より多く目を瞑ってたらダメ

import cv2
import dlib
import numpy as np
import imutils
from imutils import face_utils
from scipy.spatial import distance
import time
import copy
import os
from collections import deque
import subprocess
import sys

def calc_eye(eye):
    p2_p6 = distance.euclidean(eye[1], eye[5])
    p3_p5 = distance.euclidean(eye[2], eye[4])
    p1_p4 = distance.euclidean(eye[0], eye[3])
    EAR = (p2_p6 + p3_p5) / (2.0 * p1_p4)
    return(round(EAR,3))

def detect():
    start = time.time()
    cascadePath = "./FaceRecognition/haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(cascadePath)
    face_parts_detector = dlib.shape_predictor("./CameraTest/shape_predictor_68_face_landmarks.dat")
    detector = dlib.get_frontal_face_detector()

    cap = cv2.VideoCapture(0)

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640) # カメラ画像の横幅を640に設定
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480) # カメラ画像の縦幅を480に設定

    frame_width= cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    frame_height= cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

    minW = 0.1*cap.get(3)
    minH = 0.1*cap.get(4)

    q = deque()
    is_close = False
    n_close = 0
    n_all = 0
    while True:
        tick = cv2.getTickCount()

        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, -1)

        frame = cv2.resize(frame, dsize=(int(frame_width),int(frame_height)))
        face_frame = copy.deepcopy(frame)
        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

        faces = faceCascade.detectMultiScale( 
                gray,
                scaleFactor = 1.2,
                minNeighbors = 5,
                minSize = (int(minW), int(minH)),
            )
        # print(len(faces)==0)

        if len(faces) == 0:
            continue

        x, y, w, h = faces[0, :]
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        face = dlib.rectangle(x, y, x + w, y + h)

        face_parts_dets = face_parts_detector(gray, face)
        face_parts = face_utils.shape_to_np(face_parts_dets)

        left_eye = face_parts[42:48]
        left_eye_ear = calc_eye(left_eye)

        right_eye = face_parts[36:42]
        right_eye_ear = calc_eye(right_eye)
        
        if left_eye_ear < 0.2 or right_eye_ear < 0.2:
            print('close')
            is_close = True
        else:
            print('open')
            is_close = False

        n_all += 1
        n_close += int(is_close)
        now = time.time()

        if now-start > 600:
            return

        q.append([now, is_close])
        while now - q[0][0] > 60:
            l = q.popleft()
            n_all -= 1
            n_close -= int(l[1])

        if n_close / n_all > 0.115:
            print('寝てるやん！')
            res = subprocess.run(["python3", 'ToFirebase/getup_notify.py'], stdout=subprocess.PIPE)
            sys.stdout.buffer.write(res.stdout)
            return

        fps = cv2.getTickFrequency() / (cv2.getTickCount() - tick)
        # print(fps)