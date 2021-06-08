# 1枚写真をとってmy_pic.jpgに保存するプログラム

# -*- coding: utf-8 -*-
import time
import picamera
# import cv2 as cv

fn = 'my_pic.jpg'

# カメラ初期化
with picamera.PiCamera() as camera:
    # 解像度の設定
    camera.resolution = (512, 384)
    # 撮影の準備
    camera.start_preview()
    # 準備している間、少し待機する
    time.sleep(2)
    # 撮影して指定したファイル名で保存する
    camera.capture(fn)
    exit()