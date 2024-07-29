import re
import json
import time
import os

# 外部 ライブラリ
from fake_useragent import UserAgent
import requests
from cachecontrol import CacheControl
from cachecontrol.caches import FileCache
from bs4 import BeautifulSoup

# 自作ライブラリ
from parse_year_html import parse_year_html

# 数字か判定


def checkInt(data: str) -> bool:
    try:
        int(data)
        return True
    except ValueError:
        return False


# リクエスト送信
session = requests.Session()
# sessionをラップしたcached_sessionを作る。
# キャッシュはファイルとして .webcache ディレクトリ内に保存する。
cached_session = CacheControl(session, cache=FileCache('.webcache',forever=True))

# ユーザーエージェント
ua = UserAgent()

def request_html(url: str) -> str:
    # リクエスト送信
    response = cached_session.get(url,headers={'User-Agent': ua.chrome})

    # レスポンス取得
    response.encoding = response.apparent_encoding

    # レスポンス取得
    return response.text


with open("./htmls/index_sample.html", "r", encoding="utf-8") as read_html:
    html_content = read_html.read()

# HTMLを解析
soup = BeautifulSoup(html_content, 'html.parser')

# check index
check_index = 4

# リンクを取得
atag_elems = soup.find_all(href=re.compile(
    "www.ipa.go.jp/shiken/mondai-kaiotu"))

# 結果
result_json = {}

# リンクを表示
for atag_elem in atag_elems:
    # URL取得
    href_url = str(atag_elem.attrs['href'])

    # 末尾取得
    last_name = str(href_url.split("/")[-1])

    # 数字かどうか判定
    if (not checkInt(last_name[0:check_index])):
        # 数字じゃないとき
        continue

    # 年度取得
    year_tag = str(last_name[0:check_index])

    try:
        # 年度HTMLの保存先
        save_path = "./htmls/" + year_tag + ".html"

        if os.path.exists(save_path):
            # HTMLを取得
            html_content = request_html(href_url)

            with open(save_path, "w", encoding="utf-8") as write_html:
                write_html.write(html_content)
        else:
            with open(save_path, "r", encoding="utf-8") as read_html:
                html_content = read_html.read()

        # 年度をキーにしてJSONを追加
        result_json[year_tag] = parse_year_html(html_content)

    except Exception as ex:
        print(ex)

    print(year_tag)
    time.sleep(1)


# 結果をJSONに変換
with open("./result.json", "w", encoding="utf-8") as write_json:
    json.dump(result_json, write_json,ensure_ascii=False)