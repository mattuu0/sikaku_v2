import requests
import json
import os
import shutil
import time

dl_dir = "./auto_dl"

def ResetDir(path):
    try:
        #存在しないなら作成
        os.makedirs(path)
    except:
        import traceback
        traceback.print_exc()

# 初期化
ResetDir(dl_dir)

# だうんろーだー
def download(url, path):
    # ファイルが存在するとき
    if os.path.exists(path):
        return False

    with open(path, 'wb') as dl_file:
        res = requests.get(url)
        dl_file.write(res.content)

    return True

# json 読み込み
with open("./result.json", "r", encoding="utf-8") as read_file:
    result_json = json.load(read_file)

for key, value in result_json.items():
    # ディレクトリ名生成
    dl_path = os.path.join(dl_dir, key)

    # ディレクトリ作成
    ResetDir(dl_path)

    # 試験を回す
    for siken_tag in value.keys():
        # ディレクトリ名生成
        siken_dir = os.path.join(dl_path, siken_tag)

        # ディレクトリ作成
        ResetDir(siken_dir)

        # 時間のタグ取得
        for time_tag in value[siken_tag].keys():
            # ディレクトリ名生成
            time_dir = os.path.join(siken_dir, time_tag)

            # 試験の情報
            siken_data = value[siken_tag][time_tag]

            # ディレクトリ作成
            ResetDir(time_dir)

            #問題をダウンロード
            ans_candl = download(siken_data["qslink"],os.path.join(time_dir,siken_data["qsname"]))
            
            #解答をダウンロード
            qs_candl = download(siken_data["anslink"],os.path.join(time_dir,siken_data["ansname"]))

            print(f"Download {siken_data['qsname']} and {siken_data['ansname']}")

            # どちらかがダウンロードできたら1秒待つ
            if (qs_candl == True or ans_candl == True):
                time.sleep(1)