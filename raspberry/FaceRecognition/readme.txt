学習する際の手順

《！！！ファイル名の先頭が01~03のデータはこのディレクトリで実行する！！！》

1. 学習データ取得
$ python3 01_face_dataset.py
を実行して、学習データを作成する。30枚画像が取得できたらプログラムは終了する。
（画像はdatasetフォルダに保存される）

2. モデルの学習
$ python3 02_face_training.py
を実行して、モデルの学習を行う。

3. 認識できているかテスト
$ python3 03_face_recognition.py
を実行し、出力がいい感じなら大丈夫。
＊新たなオーナーを追加した時は、namesリストに追加して実行する。

4. face_recognition.pyのnamesリストも更新して終わり