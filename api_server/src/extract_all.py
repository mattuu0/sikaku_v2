import time
import fitz
import re
import json
import os

from tqdm import tqdm

def convert_timetag(time_tag) -> str:
    if (time_tag == "am"):
        return "午前"
    elif (time_tag == "am1"):
        return "午前Ⅰ"
    elif (time_tag == "am2"):
        return "午前Ⅱ"
    return ""

def extract(pdf_path) -> list:
    return_list = []

    # PDFの読み込み
    load_time = time.time()
    document = fitz.open(pdf_path)

    # PDFの読み込み
    print(f"Load TIme : {time.time() - load_time}")

    # 検索
    find_time = time.time()

    for page_index in range(len(document)):
        # 検索
        tables = document[page_index].find_tables()

        # 検索
        if tables.tables:
            for table in tables:
                for data in table.extract():
                    first_data = str(data[0])

                    # 検索
                    search_result = re.sub(r"\D", "", first_data)

                    # 結果が存在するか
                    if bool(search_result):
                        # 結果を返す
                        type_data = "None"

                        # 結果を返す
                        if len(data) == 3:
                            type_data = data[2]

                        # 結果を返す
                        ans = data[1]

                        # 結果を返す
                        if ans == None:
                            ans = data[3]

                        # 結果を返す
                        return_list.append(
                            {"num": search_result, "ans": ans, "type": type_data})
                    else:
                        continue
        print(f"Find Time : {time.time() - find_time}")

    return return_list

#設定
extract_path = "./datas"

# json 読み込み
with open("./result.json", "r", encoding="utf-8") as read_file:
    result_json = json.load(read_file)

#時間のタグ
time_tags = {}

# データ辞書
datas_dict = {}

for key, value in tqdm(result_json.items()):
    # ディレクトリ名生成
    dl_path = os.path.join(extract_path, key)

    # 試験を回す
    for siken_tag in tqdm(value.keys()):
        # ディレクトリ名生成
        siken_dir = os.path.join(dl_path, siken_tag)

        # tags かどうか
        if (siken_tag == "tags"):
            continue

        # 時間のタグ取得
        for time_tag in tqdm(value[siken_tag].keys()):
            try:
                # リストに含まれているか
                if not time_tag in time_tags.keys():
                    #含まれていなかったら 追加
                    time_tags[time_tag] = convert_timetag(time_tag)

                # ディレクトリ名生成
                time_dir = os.path.join(siken_dir, time_tag)

                # 試験の情報
                siken_data = value[siken_tag][time_tag]
                
                #回答を抽出
                extract_data = extract(os.path.join(time_dir, siken_data["ansname"]))

                #拡張子を分離
                # result_name = os.path.splitext(siken_data["ansname"])[0]

                # 結果を書き込む
                with open(os.path.join(time_dir,"data" + ".json"), "w", encoding="utf-8") as write_file:
                    json.dump({
                        "qsname" : siken_data["qsname"],
                        "qslink" : siken_data["qslink"],
                        "count": len(extract_data),
                        "data": extract_data
                    }, write_file, ensure_ascii=False, indent=3)

            except:
                import traceback
                traceback.print_exc()
                
                continue
    #tags copy
    tags = dict(value["tags"])

    # 試験ごとの時間
    siken_times = {}

    # 試験ごとの時間を取得
    for siken_tag in value["tags"].keys():
        try:
            siken_times[siken_tag] = list(value[siken_tag].keys())
        except:
            import traceback
            traceback.print_exc()

            #問題がないタグを削除する
            del tags[siken_tag]

            continue
    # 結果を返す
    datas_dict[key] = {
        "time_tags": time_tags,
        "tags": tags,
        "siken_times": siken_times
    }

with open(os.path.join(extract_path, "datas.json"), "w", encoding="utf-8") as write_file:
    json.dump(datas_dict, write_file, ensure_ascii=False, indent=3)