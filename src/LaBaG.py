from numpy import random 

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
        self.times = 3 #可遊玩次數 正常30
        self.played = 0 #已遊玩次數

        self.score = 0
        self.margin_score= 0

        self.Ps = [None, None, None]
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
        
        #機率區間
        def acc_rate(mode: str = "Normal") -> list[int]:
            res = list()
            acc = 0
            for p in P.Dict.values():
                acc += p.rate_dict[mode]
                res.append(acc)
            return res
        
        self.rate_ranges = {
            mode: acc_rate(mode) for mode in ["Normal", "SuperHHH", "GreenWei", "PiKaChu"]
        }
        
        #加分倍數
        self.score_times_dict = {
            "Normal": 1,
            "SuperHHH": 1,
            "GreenWei": 3,
            "PiKaChu": 1
        }
        self.score_time = 1

        #region 特殊模式
        self.ModtoScreen = False #模式影響畫面
        #超級阿禾
        self.SuperRate = 15
        self.SuperHHH = False
        self.SuperNum = 0
        self.SuperTimes = 0
        self.double_score = 0 #超級阿禾加倍分

        #綠光阿瑋
        self.GreenRate = 35
        self.GreenWei = False
        self.GreenNum = 0
        self.GreenTimes = 0
        self.GssNum = 0 #咖波累積數

        #皮卡丘
        self.PiKaChu = False
        self.kachu_times = 0

        #endregion

    def Reset(self):
        """重置"""
        self.AllData = dict()
        self.DataIndex = 0

        self.played = 0
        self.score = 0
        self.margin_score= 0
        self.score_time = 1
        self.Ps = [None, None, None]
        
        self.SuperHHH = False
        self.SuperTimes = 0

        self.GreenWei = False
        self.GreenTimes = 0
        self.GssNum = 0

        self.PiKaChu = False
        self.kachu_times = 0

    def Logic(self):
        """邏輯流程"""
        self.Reset()
        while self.GameRunning():
            self.ModtoScreen = False
            self.OneData = dict()

            self.margin_score = 0
            self.double_score  = 0
            self.Random() 
            self.CalculateScore()
            self.Result()
            self.JudgeMode()        
    
    def GameRunning(self) -> bool:
        """判斷一局遊戲是否繼續運行"""
        return self.played < self.times

    def NowMode(self)  -> str:
        """現在模式"""
        modes = {
            self.SuperHHH: "SuperHHH",
            self.GreenWei: "GreenWei",
            self.PiKaChu: "PiKaChu"
        }
        return modes.get(True, "Normal")
        

    def Random(self):
        """遊戲變數隨機產生"""
        RandNums = random.randint(1, 101, 3)
        for i in range(3):
            self.OneData[f"RandNums[{i}]"] = int(RandNums[i])

        self.SuperNum = random.randint(1, 101)
        self.OneData["SuperHHH"] = int(self.SuperNum)
        self.GreenNum = random.randint(1, 101)
        self.OneData["GreenWei"] = int(self.GreenNum)

        rate_range = self.rate_ranges[self.NowMode()]

        for i in range(3):
            for j in range(6):
                if RandNums[i] <= rate_range[j]:
                    self.Ps[i] = P.Dict[list(P.Dict.keys())[j]]
                    break

            
        #增加咖波累積數
        for p in self.Ps:
            if p.code == "A" and self.GssNum < 20 :
                self.GssNum += 1
        
    def CalculateScore(self):
        """計算分數"""
        def margin_add(p: P, typ: int):
            """p -> 使用 p 的分數列表\ntyp -> 得分型態"""
            self.margin_score += p.score_list[typ]

        match len(set(p.code for p in self.Ps)):
            case 1: #三個一樣
                margin_add(self.Ps[0], 0)
            case 2: #兩個一樣
                if self.Ps[0] == self.Ps[1]:
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
            case 3: #三個不一樣
                margin_add(self.Ps[0], 2)
                margin_add(self.Ps[1], 2)
                margin_add(self.Ps[2], 2)
                self.margin_score = round(self.margin_score / 3)

        self.score_time = self.score_times_dict[self.NowMode()]
        self.margin_score *= self.score_time
        

    def Result(self):
        """結果"""
        self.played += 1
        self.DataIndex += 1
        self.score += self.margin_score
        self.AllData[f"{self.DataIndex}"] = self.OneData
                    
    def JudgeMode(self):
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
        
        
        
        match self.NowMode():
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
                    return
                
                #判斷綠光阿瑋
                gss_all = all(p.code == "A" for p in self.Ps) #判斷是否有出現並全部咖波
                if self.GreenNum <= self.GreenRate and gss_all :
                    self.GreenWei = True
                    self.GreenTimes += 2
                    if self.PiKaChu:
                        self.PiKaChu = False
                    
                    self.ModtoScreen = True
                    return

                elif self.GssNum >= 20 : #咖波累積數達到20
                    self.GreenWei = True
                    self.GreenTimes += 2
                    self.GssNum = 0
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
                    self.JudgeMode() #判斷是否可再進入特殊模式
                    self.ModtoScreen = True

                return
            
            case "GreenWei":
                self.GreenTimes -= 1
                if all(p.code == "A" for p in self.Ps):
                    self.GreenTimes += 1
                if self.GreenTimes <= 0 : #綠光阿瑋次數用完
                    self.GreenWei = False
                    self.JudgeMode() #判斷是否可再進入特殊模式
                    self.ModtoScreen = True
                
                return
            
if __name__ == "__main__":
    Game = LaBaG()
    Game.Logic()
    print(Game.score)