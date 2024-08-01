# 環境構築方法
必要なライブラリを入れる
```
pip install beautifulsoup4
pip install cachecontrol[filecache]
pip install PyMuPDF
pip install requests
```

1. htmls フォルダを作る
2. datas フォルダを作る
3. parse_all_html.py を実行する
4. auto_dl.py を実行する
5. extract_all.py を実行する

## 注意
web/pdfjs-4.5.136-dist/web/viewer.mjs の HOSTED_VIEWER_ORIGINS に オリジンをついかする (多分pdf.jsがあるオリジン)