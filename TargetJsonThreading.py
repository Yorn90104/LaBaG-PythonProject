#產生目標分數的隨機數 json 檔
from random import randint
import math
import os
from datetime import datetime
import json
import threading
from queue import Queue
from src.Sheet import Sheet

class P:
    """圖案符號"""
    Dict = dict()

    def __init__(self, code: str = None, score_list: list[int] = None, rate_dict: dict[str, int]= None):
        self.code = code
        self.score_list = score_list or []
        self.rate_dict = rate_dict or {"Normal": 0}
        
        self.AddDict()

    def AddDict(self):
        """加入類字典中"""
        if self.code not in P.Dict:
            P.Dict[self.code] = self

        
class LaBaG:
    def __init__(self):
        self.AllData = dict() #總資料
        self.OneData = dict() #單次資料
        self.DataIndex = 0

        # 遊戲邏輯變數
        self.times = 30 #可遊玩次數 正常30
        self.played = 0 #已遊玩次數

        self.score = 0
        self.margin_score= 0

        P("A",[625, 350, 150], {
                "Normal": 36,
                "SuperHHH": 19,
                "GreenWei": 36,
                "PiKaChu": 36
            })
        
        P("B",[1250, 650, 220], {
                "Normal": 24,
                "SuperHHH": 5,
                "GreenWei": 24,
                "PiKaChu": 24
            })
        
        P("C",[2100, 1080, 380], {
                "Normal": 17,
                "SuperHHH": 19,
                "GreenWei": 17,
                "PiKaChu": 17
            })
        
        P("D",[2500, 1250, 420], {
                "Normal": 12,
                "SuperHHH": 19,
                "GreenWei": 12,
                "PiKaChu": 12
            })
        
        P("E",[10000, 5000, 1250], {
                "Normal": 8,
                "SuperHHH": 19,
                "GreenWei": 8,
                "PiKaChu": 8
            })
        
        P("F",[20000, 10000, 2500], {
                "Normal": 3,
                "SuperHHH": 19,
                "GreenWei": 3,
                "PiKaChu": 3
            })
        
        #加分倍數
        self.score_times_dict = {
            "Normal": 1,
            "SuperHHH": 1,
            "GreenWei": 3,
            "PiKaChu": 1
        }
        self.score_time = 1

        #region 特殊模式
        #超級阿禾
        self.SuperRate = 15
        self.SuperHHH = False
        self.SuperNum = 0
        self.SuperTimes = 0

        #綠光阿瑋
        self.GreenRate = 35
        self.GreenWei = False
        self.GreenNum = 0
        self.GreenTimes = 0
        self.gss_times = 0 #咖波累積數

        #皮卡丘
        self.PiKaChu = False
        self.kachu_times = 0

        #endregion

    def reset(self):
        """重置"""
        self.played = 0
        self.score = 0
        self.margin_score= 0
        self.score_time = 1
        
        self.SuperHHH = False
        self.SuperTimes = 0

        self.GreenWei = False
        self.GreenTimes = 0
        self.gss_times = 0

        self.PiKaChu = False
        self.kachu_times = 0

    def Logic(self):
        """邏輯流程"""
        self.AllData = dict()
        self.DataIndex = 0
        self.reset()
        while self.GameRunning():
            self.OneData = dict()
            self.random() 
            self.calculate_score()
            self.result()
            self.judge_mod()        
    
    def GameRunning(self) -> bool:
        """判斷一局遊戲是否繼續運行"""
        return self.played < self.times

    def now_mod(self)  -> str:
        """現在模式"""
        match True:
            case self.SuperHHH:
                return "SuperHHH"
            case self.GreenWei:
                return "GreenWei"
            case self.PiKaChu:
                return "PiKaChu"
            case _: #default
                return "Normal"
        

    def random(self):
        """遊戲變數隨機產生"""
        RandNums = [randint(1, 100), randint(1, 100), randint(1, 100)]
        for i in range(3):
            self.OneData[f"RandNums[{i}]"] = RandNums[i]

        self.SuperNum = randint(1, 100) 
        self.OneData["SuperHHH"] = self.SuperNum
        self.GreenNum = randint(1, 100) 
        self.OneData["GreenWei"] = self.GreenNum

        def acc_rate():
            res = list()
            acc = 0
            for i in P.Dict:
                acc += P.Dict[i].rate_dict[self.now_mod()]
                res.append(acc)
            return res
        
        rate_range = acc_rate()

        self.Ps = [None, None, None]
        for i in range(3):
            if RandNums[i] <= rate_range[0]:
                self.Ps[i] = P.Dict["A"]
            elif RandNums[i] <= rate_range[1]:
                self.Ps[i] = P.Dict["B"]
            elif RandNums[i] <= rate_range[2]:
                self.Ps[i] = P.Dict["C"]
            elif RandNums[i] <= rate_range[3]:
                self.Ps[i] = P.Dict["D"]
            elif RandNums[i] <= rate_range[4]:
                self.Ps[i] = P.Dict["E"]
            elif RandNums[i] <= rate_range[5]:
                self.Ps[i] = P.Dict["F"]

        #增加咖波累積數
        for p in self.Ps:
            if p.code == "A" and self.gss_times < 20 :
                self.gss_times += 1

    def calculate_score(self):
        """計算分數"""
        def margin_add(p: P, typ: int):
            """p -> 使用 p 的分數列表\ntyp -> 得分型態"""
            self.margin_score += p.score_list[typ]

        if self.Ps[0] == self.Ps[1] == self.Ps[2]:
            margin_add(self.Ps[0], 0)
        elif self.Ps[0] == self.Ps[1]:
            margin_add(self.Ps[0], 1)
            margin_add(self.Ps[2], 2)
            self.margin_score = round(self.margin_score / 1.3)
        elif self.Ps[1] == self.Ps[2]:
            margin_add(self.Ps[1], 1)
            margin_add(self.Ps[0], 2)
            self.margin_score = round(self.margin_score / 1.3)
        elif self.Ps[2] == self.Ps[0]:
            margin_add(self.Ps[2], 1)
            margin_add(self.Ps[1], 2)
            self.margin_score = round(self.margin_score / 1.3)  
        elif self.Ps[0] != self.Ps[1] != self.Ps[2]:
            margin_add(self.Ps[0], 2)
            margin_add(self.Ps[1], 2)
            margin_add(self.Ps[2], 2)
            self.margin_score = round(self.margin_score / 3)

        self.score_time = self.score_times_dict[self.now_mod()]
        self.margin_score *= self.score_time
        

    def result(self):
        """結果"""
        self.played += 1
        self.DataIndex += 1
        self.score += self.margin_score
        self.margin_score = 0
        self.AllData[f"{self.DataIndex}"] = self.OneData
                    
    def judge_mod(self):
        """判斷模式"""
        if not self.GameRunning():
            #關掉其他模式
            self.SuperHHH = False
            self.GreenWei = False

            #判斷皮卡丘充電
            if any(p.code == "E" for p in self.Ps) :
                self.PiKaChu = True
                self.played -= 5
                self.kachu_times += 1
                self.ModtoScreen = True
            else:
                self.PiKaChu = False
            return
        
        
        
        match self.now_mod():
            case "Normal" | "PiKaChu":
                #判斷超級阿禾
                hhh_appear = any(p.code == "B" for p in self.Ps) #判斷是否有任何阿禾
                if self.SuperNum <= self.SuperRate and hhh_appear:
                    self.SuperHHH = True
                    self.SuperTimes += 6
                    if self.PiKaChu:
                        self.PiKaChu = False

                    self.ModtoScreen = True

                    #超級阿禾加倍
                    if all(p.code == "B" for p in self.Ps):
                        self.double_score = int(round(self.score / 2)) * self.score_time
                        self.score += self.double_score
                
                #判斷綠光阿瑋
                gss_all = all(p.code == "A" for p in self.Ps) #判斷是否有出現並全部咖波
                if self.GreenNum <= self.GreenRate and gss_all :
                    self.GreenWei = True
                    self.GreenTimes += 2
                    if self.PiKaChu:
                        self.PiKaChu = False
                    
                    self.ModtoScreen = True
                    return

                elif self.gss_times >= 20 : #咖波累積數達到20
                    self.GreenWei = True
                    self.GreenTimes += 2
                    self.gss_times = 0
                    if self.PiKaChu:
                        self.PiKaChu = False
                    
                    self.ModtoScreen = True
                    return
            case "SuperHHH":
                self.SuperTimes -= 1

                if all(p.code == "B" for p in self.Ps):
                    self.SuperTimes += 2
                if self.SuperTimes <= 0 : #超級阿禾次數用完
                    self.SuperHHH = False
                    self.judge_mod() #判斷是否可再進入特殊模式
                    self.ModtoScreen = True

                return
            
            case "GreenWei":
                self.GreenTimes -= 1
                if all(p.code == "A" for p in self.Ps):
                    self.GreenTimes += 1
                if self.GreenTimes <= 0 : #綠光阿瑋次數用完
                    self.GreenWei = False
                    self.judge_mod() #判斷是否可再進入特殊模式
                    self.ModtoScreen = True
                
                return
            
def NewGame():
    Game = LaBaG()
    Game.Logic()
    return Game.score, Game.AllData


def SimulationGame():
    global target, recent_max, idx
    while result_queue.empty() :
        
        data = NewGame()

        with lock:
            idx += 1
            if data[0] > recent_max:
                recent_max = data[0]
            print(f"第{idx : {2 if idx < 10 else int(math.log10(idx)) + 2}}次 分數：{data[0] : 8}【目前最大值：{recent_max}】")
            # 檢查是否達到目標

            if data[0] > 1000000:
                Sheet.CommitScore('模擬測試最高分', recent_max)
            
            if data[0] >= target:
                result_queue.put(data)  # 將結果加入貯列
                break  # 如果達到目標，則退出迴圈

while True:   
    try:
        target = int (input("請輸入目標分數"))
        if target > 0:
            break
        else:
            print("目標分數必須大於 0")
    except ValueError as e:
        print(f"請輸入有效的數字: {e}")
        
idx = 0
recent_max = 0
lock = threading.Lock()
# 共享的結果儲存貯列
result_queue = Queue()

thread1 = threading.Thread(target=SimulationGame)
thread2 = threading.Thread(target=SimulationGame)

thread1.start()
thread2.start()

thread1.join()
thread2.join()

# 從結果隊列中取出結果
if result_queue.empty():
    print("模擬完成，但沒有達到目標分數。")
    exit()
else:
    try:
        result = result_queue.get(timeout=60)  # 等待 60 秒後拋出例外
    except Exception as e:
        print("未能獲取結果，隊列可能為空或超時。", e)

# 確保目錄存在
output_dir = "C:\\JsonLaBaG\\"
os.makedirs(output_dir, exist_ok=True)
# 使用時間戳作為部分文件名
timestamp = datetime.now().strftime("%Y%m%d")

with open(f"{output_dir}{result[0]}_{timestamp}.json", "w", encoding="utf-8") as file:
    json.dump(result[1], file, indent=4)

