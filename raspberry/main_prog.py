# 手順だけ先にまとめておく
# 動いた：is_owner関数、get_location関数
# 動いていない：detect_person関数（超音波センサ）とsend_location関数（androidに送信）

from FaceRecognition.face_recognition import is_owner
from DistanceDetection.distance_detection import detect_person
from GPSmodule.gps import get_location
from Sleep.detect_sleep import detect
# from ToFirebase.CurrentLocation import send_location
# from ToFirebase.Notification import notify
import time
import subprocess
import sys
import uuid

# user_id = str(uuid.uuid4())
user_id = 'AndroidUser'

def main():
    
    # このプログラムを一生続けるためのループ
    while(True):
        
        # 人が侵入するまで検知し続け、検知したらループ抜ける
        while(True):
            if(detect_person()):
                time.sleep(10)
                break

        # オーナーかを判断
        if(is_owner()):
            print('オーナーです')
            # time.sleep(10)
            # オーナーなら、車から降りる（detect_person==False）まで待つ
            while(1):
                detect() # 眠気の検知
                if(not detect_person()):
                    break

        else:
            print('オーナーではありません')
            res = subprocess.run(["python3", 'ToFirebase/raspberry_to_storage.py'], stdout=subprocess.PIPE)
            sys.stdout.buffer.write(res.stdout)
            res = subprocess.run(["python3", 'ToFirebase/Notification.py'], stdout=subprocess.PIPE)
            sys.stdout.buffer.write(res.stdout)
            # オーナーでなければ、定期的に位置情報を報告
            while(1):
                time.sleep(3) # 3秒に1回
                data = get_location() #(latitude, longitude, timestamp)
                res = subprocess.run(["python3", 'ToFirebase/CurrentLocation.py', user_id, str(data[0]), str(data[1]), str(data[2])], stdout=subprocess.PIPE)
                sys.stdout.buffer.write(res.stdout)

                #if(not detect_person()):
                    #time.sleep(10)
                    #if(not detect_person()):
                        #break

    return


if __name__ == '__main__':
    main()
