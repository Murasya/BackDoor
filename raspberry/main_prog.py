# 手順だけ先にまとめておく
# 動いた：is_owner関数、get_location関数
# 動いていない：detect_person関数（超音波センサ）とsend_location関数（androidに送信）

from GPS.gps import get_location
from FaceRecognition.face_recognition import is_owner
import time

def main():
    
    # このプログラムを一生続けるためのループ
    while(True):
        
        # 人が侵入するまで検知し続け、検知したらループ抜ける
        while(True):
            if(detect_person()):
                break

        # オーナーかを判断
        if(is_owner()):
            
            # オーナーなら、車から降りる（detect_person==False）まで待つ
            while(1):
                if(not detect_person()):
                    break

        else:
            # オーナーでなければ、定期的に位置情報を報告
            while(1):
                time.sleep(300000) # 一旦5分に1回とする
                data = get_location() #{'location':{'lat':xx, 'lng':xx}, 'accuracy':xx}
                send_location(data)

    return


if __name__ == '__main__':
    main()