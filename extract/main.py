import fitz
import re
import time
import uuid
from fastapi import FastAPI,File, UploadFile,HTTPException
import shutil
import os

# 定数
Upload_Dir = "./uptemp"

def ResetDir(path):
    try:
        #存在するか
        if os.path.exists(path):
            #存在するなら削除
            shutil.rmtree(path)

        #存在しないなら作成
        os.makedirs(path)
    except:
        import traceback
        traceback.print_exc()

# 初期化
ResetDir(Upload_Dir)

page_index = 1

def extract(pdf_path,page_index:int = 0) -> list:
    return_list = []

    # PDFの読み込み
    load_time = time.time()
    document = fitz.open(pdf_path)

    # PDFの読み込み
    print(f"Load TIme : {time.time() - load_time}")

    # 検索
    find_time = time.time()

    # 検索
    tables = document[page_index].find_tables()

    # 検索
    if tables.tables:
        for table in tables:
            for data in table.extract():
                first_data = str(data[0])

                # 検索
                search_result = re.sub(r"\D","",first_data)

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
                    return_list.append({"num":search_result,"ans":ans,"type":type_data})
                

    print(f"Find Time : {time.time() - find_time}")

    return return_list

# Fastapi のインスタンス初期化
app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/fe_extract/")
async def fe_upload_file(upfile: UploadFile = File(...)):
    #ファイル名生成
    temp_path = os.path.join(Upload_Dir,uuid.uuid4().hex + ".pdf")

    try:
        # 一時ファイルの保存
        with open(temp_path, "wb") as temp_file:
            shutil.copyfileobj(upfile.file, temp_file)

        #答え抽出
        find_answer = extract(temp_path,page_index)

        #ファイル削除
        try:
            os.remove(temp_path)
        except:
            pass

        return {
            "answer" : find_answer
        }

    except:
        import traceback
        traceback.print_exc()

    
    #ファイル削除
    try:
        os.remove(temp_path)
    except:
        pass

    raise HTTPException(status_code=500, detail="failed to extract answer")

@app.post("/sc_extract/")
@app.post("/ap_extract/")
@app.post("/sw_extract/")
@app.post("/nw_extract/")
@app.post("/sa_extract/")
@app.post("/st_extract/")
async def iroiro_gozen_upload_file(upfile: UploadFile = File(...)):
    #ファイル名生成
    temp_path = os.path.join(Upload_Dir,uuid.uuid4().hex + ".pdf")

    try:
        # 一時ファイルの保存
        with open(temp_path, "wb") as temp_file:
            shutil.copyfileobj(upfile.file, temp_file)

        #答え抽出
        find_answer = extract(temp_path,0)

        #ファイル削除
        try:
            os.remove(temp_path)
        except:
            pass

        return {
            "answer" : find_answer
        }

    except:
        import traceback
        traceback.print_exc()

    
    #ファイル削除
    try:
        os.remove(temp_path)
    except:
        pass

    raise HTTPException(status_code=500, detail="failed to extract answer")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)