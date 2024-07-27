from bs4 import BeautifulSoup
import re,os
import json

with open("./sample.html", "r",encoding="utf-8") as read_html:
    html_content = read_html.read()

#HTMLを解析
soup = BeautifulSoup(html_content, 'html.parser')

names_json = {}

# h4タグを取得
h4_elems = soup.find_all("h4")

# h4タグを表示
for h4_elem in h4_elems:
    # 内容を取得
    content = str(h4_elem.text)

    # 置き換え
    content = content.replace("（", " (")
    content = content.replace("）", ")")

    #かっこを含んでいるか判定
    if ("(" in content) and (")" in content):
        #囲まれてる文字列を取得
        tag_data = content[content.find("(") + 1 : content.find(")")]

        #小文字化
        key_tag = tag_data.lower()

        # st の場合
        if (key_tag in "st"):
            names_json["koudo"] = content

        #jsonに格納
        names_json[key_tag] = content

print(names_json)

#リンクを取得
atag_elems = soup.find_all(href=re.compile("www.ipa.go.jp/shiken/mondai-kaiotu"))

#結果
result_json = {}

#リンクを表示
for atag_elem in atag_elems:
    #URL取得
    href_url = str(atag_elem.attrs['href'])

    #ファイル名取得
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

    print(split_names)

    #午前かどうか
    if ("am" in time_tag):
        #キーが無い場合
        if (split_names[1] not in result_json):
            
            # 作成
            result_json[split_names[1]] = {}

            try:
                # 名前を取得
                result_json[split_names[1]]["name"] = names_json[split_names[1]]
            except:
                import traceback
                traceback.print_exc()

        print(split_names[-1].split(".")[0])
        # 初期化
        if (time_tag not in result_json[split_names[1]]):
            result_json[split_names[1]][time_tag] = {}

        # 回答かどうか
        if (split_names[-1].split(".")[0] == "ans"):
            result_json[split_names[1]][time_tag]["ans"] = {
                "ans" : file_name,
                "link" : href_url
            }
    
        # 問題かどうか 
        if (split_names[-1].split(".")[0] == "qs"):
            result_json[split_names[1]][time_tag]["qs"] = {
                "qs" : file_name,
                "link" : href_url
            }


# ファイルに書き込み
with open('result.json', 'w',encoding="utf-8") as out_result:
    json.dump(result_json, out_result, indent=3,ensure_ascii=False)

print(result_json)