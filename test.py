from bs4 import BeautifulSoup,element
import re

with open("./htmls/2024.html", "r", encoding="utf-8") as read_html:
    read_content = read_html.read()

soup = BeautifulSoup(read_content, 'html.parser')

for find_div in soup.find_all('div'): 
    find_div : element.Tag = find_div

    # div から aタグを取得
    find_all_atag = find_div.find_all("a")

    # a タグを取得出来たか
    if len(find_all_atag) == 0:
        # a タグを取得出来なかった場合
        continue
    
    # a タグを取得
    for atag in find_all_atag:
        atag : element.Tag = atag
        
        # a タグの href を取得
        href = atag.attrs['href']

        #pdfファイルのみを取得
        if re.search("/shiken/mondai-kaiotu", href) and re.search("^.*.pdf$", href):
            print(href)