#! /usr/bin/python
# -*- coding: utf-8 -*-
import cv2
import dlib
import numpy as np
import imutils
from imutils import face_utils
from scipy.spatial import distance
import time
import copy

face_parts_detector = dlib.shape_predictor("./shape_predictor_68_face_landmarks.dat")
detector = dlib.get_frontal_face_detector()

#カメラデバイスオープン
cap = cv2.VideoCapture(0)

# カメラフレームサイズをVGAに変更する
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640) # カメラ画像の横幅を640に設定
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480) # カメラ画像の縦幅を480に設定

# フレームサイズ取得
frame_width= cap.get(cv2.CAP_PROP_FRAME_WIDTH)
frame_height= cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

##########################
# 目が閉じているか計算する   #
##########################
def calc_eye(eye):
    p2_p6 = distance.euclidean(eye[1], eye[5])
    p3_p5 = distance.euclidean(eye[2], eye[4])
    p1_p4 = distance.euclidean(eye[0], eye[3])
    EAR = (p2_p6 + p3_p5) / (2.0 * p1_p4)
    return(round(EAR,3))

###################
# 目の中心位置算出   #
###################
def eye_center(shape):
        eyel, eyer = np.array([0, 0]), np.array([0, 0])
        # 左目の位置
        for i in range(36, 42):
            eyel[0] += shape.part(i).x
            eyel[1] += shape.part(i).y
        # 右目の位置
        for i in range(42, 48):
            eyer[0] += shape.part(i).x
            eyer[1] += shape.part(i).y
        return eyel / 6, eyer / 6

##############
# メイン処理   #
##############
while True:
    #FPS算出のため、事前に時間を取得
    tick = cv2.getTickCount()
    # カメラキャプチャー
    ret, image = cap.read()
    image = cv2.flip(image, -1) # flip video image vertically
    # 画像リサイズ
    image = cv2.resize(image,dsize=(int(frame_width),int(frame_height)))
    # リサイズした画像をコピー
    face_frame = copy.deepcopy(image)
    # グレースケール
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

    # 時間取得
    t1 = time.time()
    # 顔検出
    rects = detector(gray,1)
    t2 = time.time()

    # Dlibの顔検出箇所の矩型描画ループ
    for dets in rects:
        # オリジナル画像のランドマークを取得する
        face_parts_dets = face_parts_detector(gray, dets)
        face_parts = face_utils.shape_to_np(face_parts_dets)

        # ランドマーク68箇所に数字表示変数を初期化
        idx=1
        for (xx, yy) in face_parts:
            # 顔の1箇所毎に合計68箇所に数字
        #    cv2.putText(image, str(idx), (xx,yy),
        #        fontFace=cv2.FONT_HERSHEY_SCRIPT_SIMPLEX,
        #        fontScale=0.4,
        #        color=(100, 0, 0))
            # 顔の1箇所毎に合計68箇所にプロットする
            # cv2.circle(image, (xx,yy),2, (0,255,0), thickness= -1)

            ########################
            # 口部位を取得、表示と保存 #
            ########################
            # (x, y, w, h) = cv2.boundingRect(np.array([face_parts[48:68]])) #口の部位のみ切り出し
            # mouth = face_frame[y:y + h, x:x + w]
            # mouth = cv2.resize(mouth,(200,100))
            # # Window表示位置指定
            # cv2.moveWindow("Mouth", 850,320)
            # # 口の画像を表示
            # cv2.imshow('Mouth',mouth)
            # # 口の画像を保存
            # cv2.imwrite("./dlib_landmark_image_mouse.png",mouth)

            ##########################
            # 左目部位を取得、表示と保存 #
            ##########################
            (x, y, w, h) = cv2.boundingRect(np.array([face_parts[42:48]]))  # 左目の部位のみ切り出し
            leftEye = face_frame[y:y + h, x:x + w]
            leftEye = cv2.resize(leftEye, (200, 80))
            #  # Window表示位置指定
            # cv2.moveWindow("leftEye", 850,100)
            # # 左目の画像を表示
            # cv2.imshow('leftEye',leftEye)
            # # 左目の画像を保存
            # cv2.imwrite("./dlib_landmark_image_leftEye.png",leftEye)

            ##########################
            # 右目部位を取得、表示と保存 #
            ##########################
            (x, y, w, h) = cv2.boundingRect(np.array([face_parts[36:42]]))  # 左目の部位のみ切り出し
            rightEye = face_frame[y:y + h, x:x + w]
            rightEye = cv2.resize(rightEye, (200, 80))
            #  # Window表示位置指定
            # cv2.moveWindow("rightEye", 850,210)
            # # 右目の画像を表示
            # cv2.imshow('rightEye',rightEye)
            # # 右目の画像を保存
            # cv2.imwrite("./dlib_landmark_image_rightEye.png",rightEye)

            # ランドマーク68箇所に数字表示変数をインクリメント
            idx += 1

        ############ 左目 ###########
        left_eye = face_parts[42:48]
        left_eye_ear = calc_eye(left_eye)
        ############ 右目 ###########
        right_eye = face_parts[36:42]
        right_eye_ear = calc_eye(right_eye)

       # 両目閉じているかチェック
        if (left_eye_ear + right_eye_ear) < 0.50:
            # 目を閉じるメッセージを出力
            # cv2.putText(image, "Close Eye !!!",(10,430), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 1, cv2.LINE_AA)
            print('close')
        else:
            # 目中心位置算出とに描画
            # center_right_eye,center_left_eye = eye_center(face_parts_dets)
            # cv2.circle(image, (int(center_left_eye[0]),int(center_left_eye[1])), 3, (0, 0, 255), -1)
            # cv2.circle(image, (int(center_right_eye[0]),int(center_right_eye[1])), 3, (0, 0, 255), -1)
            print('open')

    # FPS算出と表示用テキスト作成
    fps = cv2.getTickFrequency() / (cv2.getTickCount() - tick)
    # 検出時間を算出
    detect_time = t2 - t1
    # FPS表示
    # cv2.putText(image, "FPS:{}".format(int(fps)),(10,450), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 1, cv2.LINE_AA)
    # 顔検出時間表示
    # cv2.putText(image, "DetectTime:{:.2f}".format(detect_time),(10,465), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 1, cv2.LINE_AA)
    # フレームサイズ表示
    # cv2.putText(image, str(int(frame_width))+"*"+str(int(frame_height)),(10,20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 1, cv2.LINE_AA)
    print('fps:', int(fps), ', detect_time:', int(detect_time))

    # ウィンドウに表示
    # cv2.moveWindow("DLIB_Landmark",200,100) # Window表示位置指定
    # cv2.imshow('DLIB_Landmark',image)

    # ESCキーで終了
    k = cv2.waitKey(10) & 0xff
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()
