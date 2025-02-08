#產生目標分數的隨機數 json 檔
from random import randint
import math
import os
from datetime import datetime
import json

from src.Sheet import Sheet
from src.LaBaG import LaBaG

while True:   
    try:
        target = int (input("請輸入目標分數"))
        if target > 0:
            break
        else:
            print("目標分數必須大於 0")
    except ValueError as e:
        print(f"請輸入有效的數字: {e}")

Game = LaBaG()

recent_max = 0
recent_total = 0

i = 0
while True :
    Game.Logic()

    i += 1
    recent_total = (recent_total + Game.score) % 1000000000000000

    if Game.score > recent_max:
        recent_max = Game.score
    print(f"第{i : {2 if i < 10 else int (round(math.log10(i)) + 2)}}次 分數：{Game.score : 8}【目前最大值：{recent_max}】【目前平均值：{recent_total / i % 1000000000000000 :.2f}】")

    # 檢查是否達到目標
    if Game.score >= target:
        break  # 如果達到目標，則退出迴圈
    

if Game.score > 1000000:
    Sheet.CommitScore('模擬測試最高分', Game.score)

# 確保目錄存在
output_dir = "C:\\JsonLaBaG\\"
os.makedirs(output_dir, exist_ok=True)
# 使用時間戳作為部分文件名
timestamp = datetime.now().strftime("%Y%m%d")

with open(f"{output_dir}{Game.score}_{timestamp}.json", "w", encoding="utf-8") as file:
    json.dump(Game.AllData, file, indent=4)

        
     

            