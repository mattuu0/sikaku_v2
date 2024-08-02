from dotenv import load_dotenv
load_dotenv()

import os
import json

# 自身のディレクトリに移動
try:
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
except:
    pass

with open("./datas/datas.json", "r", encoding="utf-8") as read_file:
    siken_datas = json.load(read_file)

with open("./datas/datasv2.json", "r", encoding="utf-8") as read_file:
    siken_datas_v2 = json.load(read_file)

from fastapi import FastAPI,Request,HTTPException
from fastapi.responses import JSONResponse
import uvicorn
from appwrite.client import Client
from appwrite.services.account import Account


app = FastAPI()

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    try:
        # クライアント生成
        client = Client()

        # クライアント設定
        (client
            .set_endpoint(os.environ["APPWRITE_ENDPOINT"]) # Your API Endpoint
            .set_project(os.environ["APPWRITE_PROJECT_ID"]) # Your project ID
            .set_jwt(request.headers.get("actoken")) # Your secret JSON Web Token
        )

        # アカウント情報取得
        account = Account(client)

        # アカウント情報取得
        result = account.get()

        # メールが認証されているか
        if (not result["emailVerification"]):
            #認証されていないとき
            raise HTTPException(status_code=401, detail="認証されていません")
        
        # メールを検証
        if (not str(result["email"]).endswith("@ecc.ac.jp")):
            # ecc.ac.jp ではないとき
            raise HTTPException(status_code=401, detail="認証されていません")
        
        return await call_next(request)
    except:
        import traceback
        traceback.print_exc()

        return JSONResponse(
            status_code=401,
            content={"success": False}
        )
    # response = await call_next(request)
    # return response

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
    # read_json["qslink"] = f"/app/qspdf/{year}/{sikentag}/{time_tag}"

    return read_json

@app.get("/sikens")
async def sikens():
    # 返す用の辞書
    return_dict = {}

    for siken_tag in siken_datas_v2.keys():
        try:
            return_dict[siken_tag] = siken_datas_v2[siken_tag]["name"]
        except:
            import traceback
            traceback.print_exc()

            continue
    
    return return_dict

@app.get("/years/{sikentag}")
async def years(sikentag:str):
    # 試験の年度を返す
    return list(siken_datas_v2[sikentag]["years"])

# @app.get("/qspdf/{year}/{sikentag}/{time_tag}")
# async def siken_times(year:str,sikentag:str,time_tag:str):
#     # 年度の情報取得
#     if not year in siken_datas.keys():
#         # 年度がないとき
#         return {
#             "success": False
#         }

#     # 年度情報取得
#     year_data = siken_datas[year]

#     # 試験のタグが含まれているか
#     if not sikentag in year_data["tags"].keys():
#         # 試験のタグが含まれていないとき
#         return {
#             "success": False
#         }
    
#     # 時間のタグが含まれているか
#     if not time_tag in year_data["time_tags"].keys():
#         # 時間のタグが含まれていないとき
#         return {
#             "success": False
#         }
    
#     # json を読み込む
#     with open(f"./datas/{year}/{sikentag}/{time_tag}/data.json", "r", encoding="utf-8") as read_file:
#         read_json = json.load(read_file)
    
#     # 問題名を取得
#     qsname = read_json["qsname"]

#     # pdf を返す
#     return FileResponse(path=f"./datas/{year}/{sikentag}/{time_tag}/{qsname}", media_type="application/pdf")


if __name__ == "__main__":
    uvicorn.run("api_server:app", host="0.0.0.0", port=3001, log_level="debug",reload=False)
