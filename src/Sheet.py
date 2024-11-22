#https://script.google.com/macros/s/AKfycbzWA0mMx_B14vrHGW6-QK4tOClSIj1lw7udLJwp7XCg2nZ8hDxt7d-dqnc6WenqBM8FBA/exec

import subprocess
import requests 

GetData = []
data_dict = dict()

def commit_score(name, score):
    """上傳資料至試算表"""
    if name != "" :
        url = f"https://docs.google.com/forms/d/18dVGtPExBUc0p1VbsmMxCyujQoldI6GKQWZQGJQ-yzY/formResponse?entry.582969025={name}&entry.995493130={score}"
        subprocess.Popen(['curl', url], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("資料已上傳")
    else:
        print("名稱為空，資料未上傳！")

def tide_data():
    """整理資料至字典"""
    global GetData, data_dict
    del GetData[0] #刪除第一列的欄名
    for row in GetData : #對每一列的資料做
        del row[0]  #刪除第一格的"時間戳記"

        if row[0] != "" and row[1] != "" :#不為空
            name = str(row[0]) #將名稱那格變為字串型態
            score = int(row[1]) #將分數那格變為整數型態
            if name in data_dict :
                if score > data_dict[name] :
                    data_dict[name] = score
            else :
                data_dict[name] = score
    
    for d in data_dict :
        print(f"{d}：{data_dict[d]:6}")
        
def get_data():
    """從試算表抓取原資料"""
    global GetData
    web = requests.get("https://script.google.com/macros/s/AKfycbzWA0mMx_B14vrHGW6-QK4tOClSIj1lw7udLJwp7XCg2nZ8hDxt7d-dqnc6WenqBM8FBA/exec")
    GetData = web.json()

    tide_data()

def find_history_score(name = ""):
        """找歷史分數資料"""
        global data_dict
        if name != "" :
            if name in data_dict: #檢查是否已在字典裡
                return data_dict[name]
            else : #沒有就新增一個
                data_dict[name] = 0
                return data_dict[name]
        else:
            return 0