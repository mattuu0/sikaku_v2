from bs4 import BeautifulSoup
import re
import os
import json

# 自作ライブラリ
from converter import convert_time

def parse_year_html(html_content:str):
    # HTMLを解析
    soup = BeautifulSoup(html_content, 'html.parser')

    names_json = {}

    # h4タグを取得
    h4_elems = soup.find_all("h4")

    # h4タグを表示
    for h4_elem in h4_elems:
        # 内容を取得
        content = str(h4_elem.text)

        # 置き換え
        content = content.replace("（", "(")
        content = content.replace("）", ")")

        print(content)
        # かっこを含んでいるか判定
        if ("(" in content) and (")" in content):
            # 囲まれてる文字列を取得
            tag_data = content[content.find("(") + 1: content.find(")")]

            # 小文字化
            key_tag = tag_data.lower()

            # st の場合
            if (key_tag in "st"):
                names_json["koudo"] = content

            # jsonに格納
            names_json[key_tag] = content

    print(names_json)

    # リンクを取得
    atag_elems = soup.find_all(href=re.compile(
        "/shiken/mondai-kaiotu"))

    # 結果
    result_json = {}

    # リンクを表示
    for atag_elem in atag_elems:
        # URL取得
        href_url = str(atag_elem.attrs['href'])

        # ファイル名取得
        file_name = str(href_url.split("/")[-1])

        # ファイル名分割
        split_names = file_name.split("_")

        # html の場合戻る
        if (os.path.splitext(split_names[-1])[-1] == ".html"):
            continue

        # 3つ以下の場合戻る
        if (len(split_names) < 3):
            continue

        # 時間のタグ
        time_tag = split_names[2]

        # 午前かどうか
        if ("am" in time_tag):
            # キーが無い場合
            if (split_names[1] not in result_json):

                # 作成
                result_json[split_names[1]] = {}

                try:
                    # 名前を取得
                    result_json[split_names[1]]["name"] = names_json[split_names[1]]
                except:
                    import traceback
                    traceback.print_exc()

            # 初期化
            if (time_tag not in result_json[split_names[1]]):
                result_json[split_names[1]][time_tag] = {    
                    "timejp" : convert_time(time_tag)
                }

            #回答かどうか
            data_key = split_names[-1].split(".")[0]

            # jsonに格納
            result_json[split_names[1]][time_tag][data_key] = {
                "name": file_name,
                "link": "https://www.ipa.go.jp" + href_url,
            }

    return result_json

if __name__ == "__main__":    
    with open("./htmls/2024.html", "r", encoding="utf-8") as read_html:
        read_content = read_html.read()

    print(parse_year_html(read_content))