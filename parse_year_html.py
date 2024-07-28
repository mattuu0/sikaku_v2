from bs4 import BeautifulSoup
import re
import os
import json

# 自作ライブラリ
from converter import convert_time


def parse_a(atag_elem) -> dict:
    # URL取得
    href_url = str(atag_elem.attrs['href'])

    # ファイル名取得
    file_name = str(href_url.split("/")[-1])

    # ファイル名分割
    split_names = file_name.split("_")

    # html の場合戻る
    if (os.path.splitext(split_names[-1])[-1] != ".pdf"):
        return {
            "success": False
        }

    # 3つ以下の場合戻る
    if (len(split_names) < 3):
        return {
            "success": False
        }

    # 時間のタグ
    time_tag = split_names[2]

    # 午前かどうか
    if ("am" in time_tag):
        # 試験のタグ取得
        siken_tag = split_names[1]

        return {
            "success": True,
            "siken_tag": siken_tag,
            "time_tag": time_tag,
            "file_name": file_name,
            "link" : "https://www.ipa.go.jp" + href_url
        }

    return {
        "success": False
    }

def url_to_typetag(url: str) -> str:
    return url.split("/")[-1].split("_")[-1].split(".")[0]

def parse_year_html(html_content: str):
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

            # jsonに格納
            names_json[key_tag] = content


    # リンクを取得
    atag_elems = soup.find_all(href=re.compile(
        "/shiken/mondai-kaiotu"))

    # 結果
    result_json = {}

    count = 0
    # リンクを表示
    for i in range(len(atag_elems)):
        try:
            if (count >= len(atag_elems)):
                break

            # リンクを取得
            atag_elem = atag_elems[count]

            # parse
            parse_data = dict(parse_a(atag_elem))

            #成功しない場合
            if (not parse_data["success"]):
                count += 1
                continue
            
            #koudo の時
            if (parse_data["siken_tag"] == "koudo"):
                #リンク取得
                href = parse_data["link"]

                # 問題か答えか
                typetag = url_to_typetag(href)

                # 問題の時
                if (typetag == "qs"):
                    # 高度の答えを解析
                    koudo_ans_parse = parse_a(atag_elems[count + 1])

                    # 試験の問題を解析
                    siken_qs_parse = parse_a(atag_elems[count + 2])

                    # 試験の答えを解析
                    siken_ans_parse = parse_a(atag_elems[count + 3])

                    result_json[siken_qs_parse["siken_tag"]] = {
                        parse_data["time_tag"] : {
                            "qsname" : parse_data["file_name"],
                            "qslink" : parse_data["link"],
                            "ansname" : koudo_ans_parse["file_name"],
                            "anslink" : koudo_ans_parse["link"],
                        },
                        siken_qs_parse["time_tag"] : {
                            "qsname" : siken_qs_parse["file_name"],
                            "qslink" : siken_qs_parse["link"],
                            "ansname" : siken_ans_parse["file_name"],
                            "anslink" : siken_ans_parse["link"],
                        }
                    }

                    #カウンタを進める
                    count += 4
                    continue
            else:
                # 試験の解答を解析
                siken_ans_parse = parse_a(atag_elems[count + 1])

                #jsonに格納
                result_json[parse_data["siken_tag"]] = {
                    parse_data["time_tag"] : {
                        "qsname" : parse_data["file_name"],
                        "qslink" : parse_data["link"],
                        "ansname" : siken_ans_parse["file_name"],
                        "anslink" : siken_ans_parse["link"],
                    }
                }
        except:
            import traceback
            traceback.print_exc()

            continue

        # カウンタを進める
        count += 2
    
    return result_json


if __name__ == "__main__":
    with open("./htmls/2024.html", "r", encoding="utf-8") as read_html:
        read_content = read_html.read()

    with open("./2024.json", "w", encoding="utf-8") as write_json:
        parse_data = parse_year_html(read_content)

        print(parse_data)

        json.dump(parse_data,
                  write_json, indent=3, ensure_ascii=False)
