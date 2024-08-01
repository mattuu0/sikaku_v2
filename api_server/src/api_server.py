import os
import json

with open("./datas/datas.json", "r", encoding="utf-8") as read_file:
    siken_datas = json.load(read_file)

from fastapi import FastAPI
from fastapi.responses import FileResponse
import uvicorn
from starlette.middleware.cors import CORSMiddleware # 追加

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,   # 追記により追加
    allow_methods=["*"],      # 追記により追加
    allow_headers=["*"]       # 追記により追加
)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/years")
async def years():
    # 試験の年度を返す
    return list(siken_datas.keys())

@app.get("/sikens/{year}")
async def sikens(year:str):
    # 指定の年度の試験を返す
    return siken_datas[year]["tags"]

@app.get("/times/{year}/{sikentag}")
async def siken_times(year:str,sikentag:str):
    # 試験会の時間を返す
    times = {}

    # 試験の時間を回す
    for time_tag in siken_datas[year]["siken_times"][sikentag]:
        times[time_tag] = siken_datas[year]["time_tags"][time_tag]

    # 指定の年度の試験を返す
    return times

@app.get("/siken/{year}/{sikentag}/{time_tag}")
async def siken_times(year:str,sikentag:str,time_tag:str):
    # 年度の情報取得
    if not year in siken_datas.keys():
        # 年度がないとき
        return {
            "success": False
        }

    # 年度情報取得
    year_data = siken_datas[year]

    # 試験のタグが含まれているか
    if not sikentag in year_data["tags"].keys():
        # 試験のタグが含まれていないとき
        return {
            "success": False
        }
    
    # 時間のタグが含まれているか
    if not time_tag in year_data["time_tags"].keys():
        # 時間のタグが含まれていないとき
        return {
            "success": False
        }

    # パスを生成する
    with open(f"./datas/{year}/{sikentag}/{time_tag}/data.json", "r", encoding="utf-8") as read_file:
        read_json = json.load(read_file)
    
    # 問題のリンクを設定
    read_json["qslink"] = f"http://127.0.0.1:8000/qspdf/{year}/{sikentag}/{time_tag}"

    return read_json

@app.get("/qspdf/{year}/{sikentag}/{time_tag}")
async def siken_times(year:str,sikentag:str,time_tag:str):
    # 年度の情報取得
    if not year in siken_datas.keys():
        # 年度がないとき
        return {
            "success": False
        }

    # 年度情報取得
    year_data = siken_datas[year]

    # 試験のタグが含まれているか
    if not sikentag in year_data["tags"].keys():
        # 試験のタグが含まれていないとき
        return {
            "success": False
        }
    
    # 時間のタグが含まれているか
    if not time_tag in year_data["time_tags"].keys():
        # 時間のタグが含まれていないとき
        return {
            "success": False
        }
    
    # json を読み込む
    with open(f"./datas/{year}/{sikentag}/{time_tag}/data.json", "r", encoding="utf-8") as read_file:
        read_json = json.load(read_file)
    
    # 問題名を取得
    qsname = read_json["qsname"]

    # pdf を返す
    return FileResponse(path=f"./datas/{year}/{sikentag}/{time_tag}/{qsname}", media_type="application/pdf")


if __name__ == "__main__":
    uvicorn.run("api_server:app", host="127.0.0.1", port=8080, log_level="debug",reload=True)
