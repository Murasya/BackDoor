# 動画ならこっち

import cv2
import dlib
import numpy as np
import imutils
from imutils import face_utils
from scipy.spatial import distance
import time
import copy
import os

def calc_eye(eye):
    p2_p6 = distance.euclidean(eye[1], eye[5])
    p3_p5 = distance.euclidean(eye[2], eye[4])
    p1_p4 = distance.euclidean(eye[0], eye[3])
    EAR = (p2_p6 + p3_p5) / (2.0 * p1_p4)
    return(round(EAR,3))

cascadePath = "../FaceRecognition/haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath)
face_parts_detector = dlib.shape_predictor("../CameraTest/shape_predictor_68_face_landmarks.dat")
detector = dlib.get_frontal_face_detector()

cap = cv2.VideoCapture('test.mp4')

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640) # カメラ画像の横幅を640に設定
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480) # カメラ画像の縦幅を480に設定

frame_width= cap.get(cv2.CAP_PROP_FRAME_WIDTH)
frame_height= cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

minW = 0.1*cap.get(3)
minH = 0.1*cap.get(4)

t1 = time.time()
n_all = 0
n_close_eye = 0
while True:

    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, -1)
    
    # cv2.imwrite('a.jpg', frame)
    # break
    
    frame = cv2.resize(frame, dsize=(int(frame_width),int(frame_height)))
    face_frame = copy.deepcopy(frame)
    gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

    faces = faceCascade.detectMultiScale( 
            gray,
            scaleFactor = 1.2,
            minNeighbors = 5,
            minSize = (int(minW), int(minH)),
        )
    print(len(faces)==0)
    
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
    
    n_all += 1
    if left_eye_ear < 0.2 or right_eye_ear < 0.2:
        n_close_eye += 1

t2 = time.time()
print(t2-t1)
print(n_close_eye, n_all)