import os
import json

#設定
dl_dir = "./auto_dl"

# json 読み込み
with open("./result.json", "r", encoding="utf-8") as read_file:
    result_json = json.load(read_file)

#時間のタグ
time_tags = {}

for key, value in result_json.items():
    # ディレクトリ名生成
    dl_path = os.path.join(dl_dir, key)

    # 試験を回す
    for siken_tag in value.keys():
        # ディレクトリ名生成
        siken_dir = os.path.join(dl_path, siken_tag)

        # tags かどうか
        if (siken_tag == "tags"):
            continue

        # 時間のタグ取得
        for time_tag in value[siken_tag].keys():
            print(time_tag)