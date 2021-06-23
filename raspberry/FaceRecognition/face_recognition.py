# 1分認証して、一度もオーナーである確率が高く（類似度40％以上に）ならなかったらFalse、そうでなかったらTrue

import cv2
import numpy as np
import os 
import time

def is_owner():
    have_saved = False

    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read('./FaceRecognition/trainer/trainer.yml')
    cascadePath = "./FaceRecognition/haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(cascadePath);

    font = cv2.FONT_HERSHEY_SIMPLEX

    #iniciate id counter
    id = 0

    # names related to ids: example ==> Marcelo: id=1,  etc
    names = ['None', 'Soichi'] 

    # Initialize and start realtime video capture
    cam = cv2.VideoCapture(0)
    cam.set(3, 640) # set video widht
    cam.set(4, 480) # set video height

    # Define min window size to be recognized as a face
    minW = 0.1*cam.get(3)
    minH = 0.1*cam.get(4)

    start = time.time()
    while True:
        now = time.time() - start
        if now >= 60:
            cam.release()
            cv2.destroyAllWindows()
            return False

        ret, img = cam.read()
        img = cv2.flip(img, -1) # Flip vertically

        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

        faces = faceCascade.detectMultiScale( 
            gray,
            scaleFactor = 1.2,
            minNeighbors = 5,
            minSize = (int(minW), int(minH)),
        )

        for(x,y,w,h) in faces:

            cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)

            id, confidence = recognizer.predict(gray[y:y+h,x:x+w])

            # Check if confidence is less them 100 ==> "0" is perfect match 
            if (confidence < 100):
                id = names[id]
                confidence = "  {0}%".format(round(100 - confidence))
            else:
                id = "unknown"
                confidence = "  {0}%".format(round(100 - confidence))
            
            # cv2.putText(img, str(id), (x+5,y-5), font, 1, (255,255,255), 2)
            # cv2.putText(img, str(confidence), (x+5,y+h-5), font, 1, (255,255,0), 1)  
            print(id, confidence)
            if id in names and int(confidence[:-1]) > 40:
                cam.release()
                cv2.destroyAllWindows()
                return True
            elif not have_saved:
                cv2.imwrite('./test_image.png', img)
                have_saved = True