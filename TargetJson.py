#產生目標分數的隨機數 json 檔
from random import randint
import sys , math
sys.stdout.reconfigure(encoding='utf-8')
from random import randint #隨機數字
import json

import subprocess
def commit_score(name, score):
    """上傳資料至試算表"""
    if name != "" :
        url = f"https://docs.google.com/forms/d/18dVGtPExBUc0p1VbsmMxCyujQoldI6GKQWZQGJQ-yzY/formResponse?entry.582969025={name}&entry.995493130={score}"
        subprocess.Popen(['curl', url], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("資料已上傳")
    else:
        print("名稱為空，資料未上傳！")



class P:
    def __init__(self, code: str = None, score_list: list[int] = None, rate_dict: dict[str, int]= 0):
        self.code = code
        self.score_list = score_list
        self.rate_dict = rate_dict or {"Normal": 0}

    def __str__(self):
        return self.code

        
class LaBaG:
    def __init__(self):
        self.AllData = dict() #總資料
        self.OneData = dict() #單次資料

        # 遊戲邏輯變數
        self.times = 30 #可遊玩次數 正常30
        self.played = 0 #已遊玩次數

        self.score = 0
        self.margin_score= 0

        self.P_dict = {
            "Gss":P("A",[625, 350, 150], {
                "Normal": 36,
                "SuperHHH": 19,
                "GreenWei": 36,
                "PiKaChu": 36
            }),
            "Hhh":P("B",[1250, 650, 220], {
                "Normal": 24,
                "SuperHHH": 5,
                "GreenWei": 24,
                "PiKaChu": 24
            }),
            "Hentai":P("C",[2100, 1080, 380], {
                "Normal": 17,
                "SuperHHH": 19,
                "GreenWei": 17,
                "PiKaChu": 17
            }),
            "Handsun":P("D",[2500, 1250, 420], {
                "Normal": 12,
                "SuperHHH": 19,
                "GreenWei": 12,
                "PiKaChu": 12
            }),
            "Kachu":P("E",[10000, 5000, 1250], {
                "Normal": 8,
                "SuperHHH": 19,
                "GreenWei": 8,
                "PiKaChu": 8
            }),
            "Rrr":P("F",[20000, 10000, 2500], {
                "Normal": 3,
                "SuperHHH": 19,
                "GreenWei": 3,
                "PiKaChu": 3
            }),
        }

        #加分倍數
        self.score_times_dict = {
            "Normal": 1,
            "SuperHHH": 1,
            "GreenWei": 3,
            "PiKaChu": 1
        }

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
        self.AllData = dict()
        
        self.played = 0
        self.score = 0
        self.margin_score= 0
        
        self.SuperHHH = False
        self.SuperTimes = 0

        self.GreenWei = False
        self.GreenTimes = 0
        self.gss_times = 0

        self.PiKaChu = False
        self.kachu_times = 0

    def Logic(self):
        """邏輯流程"""
        while self.GameRunning():
            self.OneData = dict()
            self.random() 
            self.judge_super()
            self.calculate_score()
            self.judge_green()
            self.result()
            self.judge_kachu()
        
    
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

        def acc_rate():
            res = list()
            acc = 0
            for i in self.P_dict:
                acc += self.P_dict[i].rate_dict[self.now_mod()]
                res.append(acc)
            return res
        
        rate_range = acc_rate()

        self.Ps = [None, None, None]
        for i in range(3):
            if RandNums[i] <= rate_range[0]:
                self.Ps[i] = self.P_dict["Gss"]
            elif RandNums[i] <= rate_range[1]:
                self.Ps[i] = self.P_dict["Hhh"]
            elif RandNums[i] <= rate_range[2]:
                self.Ps[i] = self.P_dict["Hentai"]
            elif RandNums[i] <= rate_range[3]:
                self.Ps[i] = self.P_dict["Handsun"]
            elif RandNums[i] <= rate_range[4]:
                self.Ps[i] = self.P_dict["Kachu"]
            elif RandNums[i] <= rate_range[5]:
                self.Ps[i] = self.P_dict["Rrr"]

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

        score_times = self.score_times_dict[self.now_mod()]
        self.margin_score *= score_times
        

    def result(self):
        """結果"""
        self.played += 1
        self.score += self.margin_score
        self.margin_score = 0
        self.AllData[f"{self.played}"] = self.OneData

    #region 超級阿禾模式(SuperHHH)
    def SuperFalse(self):
        self.SuperHHH = False

    def SuperRandom(self):
        self.SuperNum = randint(1, 100) #隨機數
        self.OneData["SuperHHH"] = self.SuperNum

    def judge_super(self):
        """判斷超級阿禾"""
        if not self.GameRunning:
            self.SuperFalse()
            return
        
        self.SuperFalse()
        match self.now_mod():
            case "SuperHHH":
                self.SuperTimes -= 1

                if all(p.code == "B" for p in self.Ps):
                    self.SuperTimes += 2
                if self.SuperTimes <= 0 : #超級阿禾次數用完
                    self.SuperFalse()


            case "Normal" | "PiKaChu":
                hhh_appear = any(p.code == "B" for p in self.Ps) #判斷是否有出現阿和
                if self.SuperNum <= self.SuperRate and hhh_appear:
                    self.SuperHHH = True
                    self.SuperTimes += 6
                    if self.PiKaChu:
                        self.KachuFalse()


                    #超級阿禾加倍
                    if all(p.code == "B" for p in self.Ps):
                        double_score = int(round(self.score / 2))
                        self.margin_score += double_score
            
    #endregion

    #region 綠光阿瑋模式(GreenWei)
    def GreenFalse(self):
        self.GreenWei = False

    def GreenRandom(self):
        self.GreenNum = randint(1, 100) #隨機數
        self.OneData["GreenWei"] = self.GreenNum

    def judge_green(self):
        """判斷綠光阿瑋"""
        if not self.GameRunning():
            self.GreenFalse()
            return
        
        #增加咖波累積數
        for p in self.Ps:
            if p.code == "A" and self.gss_times < 20 :
                self.gss_times += 1

        self.GreenRandom()
        match self.now_mod():
            case "GreenWei":
                self.GreenTimes -= 1
                if all(p.code == "A" for p in self.Ps):
                    self.GreenTimes += 1
                if self.GreenTimes <= 0 : #綠光阿瑋次數用完
                    self.GreenFalse()
                    self.judge_super()


            case "Normal" | "PiKaChu":
                gss_all = all(p.code == "A" for p in self.Ps) #判斷是否有出現並全部咖波
                if self.GreenNum <= self.GreenRate and gss_all :
                    self.GreenWei = True
                    self.GreenTimes += 2
                    if self.PiKaChu:
                        self.KachuFalse()
                    

                elif self.gss_times >= 20 : #咖波累積數達到20
                    self.GreenWei = True
                    self.GreenTimes += 2
                    self.gss_times = 0
                    if self.PiKaChu:
                        self.KachuFalse()
                    

    #endregion

    #region 皮卡丘充電區(PiKaChu)
    def KachuFalse(self):
        self.PiKaChu = False

    def judge_kachu(self):
        """判斷皮卡丘"""
        if not self.GameRunning() and any(p.code == "E" for p in self.Ps) :
            self.PiKaChu = True
            self.played -= 5
            self.kachu_times += 1
            #關掉其他模式
            self.SuperFalse()
            self.GreenFalse()

        else:
            self.PiKaChu = False
    #endregion
        
target = int (input("請輸入目標分數"))

Game = LaBaG()

recent_max = 0

i = 0
while True :
    i += 1
    if i < 10 :
        LOG = 2
    else:
        LOG = int (round(math.log10(i)) + 2)
    Game.reset()
    Game.Logic()

    print(f"第{i : {LOG}}次 分數：{Game.score : 8}【目前最大值：{recent_max}】")
    # 檢查是否達到目標
    if Game.score >= target:
        break  # 如果達到目標，則退出迴圈
    elif Game.score > recent_max:
        recent_max = Game.score
        if recent_max >= 1000000:
             commit_score('模擬測試最高分', recent_max)

with open("target.json", "w", encoding="utf-8") as file:
    json.dump(Game.AllData, file, indent=4)

        
     

            