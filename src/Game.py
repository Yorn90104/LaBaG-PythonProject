try:
    from src.LaBaG import P, LaBaG
except ModuleNotFoundError:
    from LaBaG import P, LaBaG

class PlayLaBaG(LaBaG):
    def __init__(self):
        super().__init__()
        self.Name = ""
        self.history_score = 0

    def Reset(self):
        super().Reset()
        self.history_score = 0

    def Logic(self):
        self.ModtoScreen = False
        self.OneData = dict()
        self.margin_score = 0
        self.double_score  = 0
        self.Random() 
        self.CalculateScore()
        self.Result()
        self.JudgeMode()

    def Random(self):
        """隨機生成數字"""
        super().Random()
        print(f"機率區間：{self.rate_ranges[self.NowMode()]}")
        print(f"超級阿禾隨機數為: {self.SuperNum}")
        print(f"綠光阿瑋隨機數為: {self.GreenNum}")
        print(f"咖波累積數：{self.GssNum}")


    def CalculateScore(self):
        """計算分數"""
        super().CalculateScore()
        print(f"加分倍數: {self.score_time}")

    def Result(self):
        """結果"""
        super().Result()
        print(f"")
        print(f' | {self.Ps[0].code} | {self.Ps[1].code} | {self.Ps[2].code} |')
        print(f"+{self.margin_score}")
        print(f"目前分數：{self.score}")
        print(f"剩餘次數：{self.times - self.played}")

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
                print(f"皮卡丘為你充電")
                print(f"已觸發 {self.kachu_times} 次皮卡丘充電")
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
                    print(f"超級阿禾出現")
                    if self.PiKaChu:
                        self.PiKaChu = False

                    self.ModtoScreen = True

                    #超級阿禾加倍
                    if all(p.code == "B" for p in self.Ps):
                        self.double_score = int(round(self.score / 2)) * self.score_time
                        self.score += self.double_score
                        if self.score_time == 3:
                            print(f"(超級阿禾 x 綠光阿瑋加倍分:{self.double_score})")
                        else:
                            print(f"(超級阿禾加倍分:{self.double_score})")
                    return
                    
                
                #判斷綠光阿瑋
                gss_all = all(p.code == "A" for p in self.Ps) #判斷是否有出現並全部咖波
                if self.GreenNum <= self.GreenRate and gss_all :
                    self.GreenWei = True
                    self.GreenTimes += 2
                    print(f"綠光阿瑋出現")
                    if self.PiKaChu:
                        self.PiKaChu = False
                    
                    self.ModtoScreen = True
                    return

                elif self.GssNum >= 20 : #咖波累積數達到20
                    self.GreenWei = True
                    self.GreenTimes += 2
                    print(f"綠光阿瑋出現")
                    self.GssNum = 0
                    if self.PiKaChu:
                        self.PiKaChu = False
                    
                    self.ModtoScreen = True
                    return
            case "SuperHHH":
                self.SuperTimes -= 1
                if all(p.code == "B" for p in self.Ps):
                    self.SuperTimes += 2
                    print("全阿禾，次數不消耗且+1！")
                print(f"超級阿禾剩餘次數:{self.SuperTimes}次")

                if self.SuperTimes <= 0 : #超級阿禾次數用完
                    self.SuperHHH = False
                    self.JudgeMode() #判斷是否可再進入特殊模式
                    self.ModtoScreen = True

                return
            
            case "GreenWei":
                self.GreenTimes -= 1
                if all(p.code == "A" for p in self.Ps):
                    self.GreenTimes += 1
                    print("全咖波，次數不消耗！")
                print(f"綠光阿瑋剩餘次數:{self.GreenTimes}次")
                
                if self.GreenTimes <= 0 : #綠光阿瑋次數用完
                    self.GreenWei = False
                    self.JudgeMode() #判斷是否可再進入特殊模式
                    self.ModtoScreen = True
                
                return
        
    def GameOver(self):
        """遊戲結束"""
        print("")
        print(f"遊戲已結束，最終分數為：{self.score}。")
        if self.score > self.history_score:
            self.history_score = self.score

#region JsonLaBaG
import json
from numpy import random 

class JsonLaBaG(PlayLaBaG):
    """與json檔案連接的啦八機"""
    def __init__(self):
        super().__init__()
        self.json_data = dict()
        self.index = "1" # 第 n 次的索引
        

    def Reset(self):
        """重置"""
        self.played = 0
        self.score = 0
        self.margin_score= 0
        self.Ps = [None, None, None]
        
        self.SuperHHH = False
        self.SuperTimes = 0

        self.GreenWei = False
        self.GreenTimes = 0
        self.GssNum = 0

        self.PiKaChu = False
        self.kachu_times = 0

        self.BeginAble = True
        self.index = "1" # 第 n 次的索引


    def setup_path(self, jsondata_path: str = None):
        """設置檔案路徑"""
        with open(jsondata_path, "r", encoding="utf-8") as json_file:
            self.json_data = json.load(json_file)
            print(f"已設置路徑為：{jsondata_path}")
    
    def index_plus(self):
        """索引值 +1"""
        self.index = str(int(self.index) + 1)

    def Random(self):
        """遊戲變數隨機產生"""
        if self.index not in self.json_data:
            return super().Random()
        RandNums = [self.json_data[self.index]["RandNums[0]"], self.json_data[self.index]["RandNums[1]"], self.json_data[self.index]["RandNums[2]"]]
        self.SuperNum = self.json_data[self.index]["SuperHHH"]
        self.GreenNum = self.json_data[self.index]["GreenWei"]

        print(f"P隨機數為：{RandNums[0]} | {RandNums[1]} | {RandNums[2]}")
        print(f"超級阿禾隨機數為: {self.SuperNum}")
        print(f"綠光阿瑋隨機數為: {self.GreenNum}")
        
        rate_range = self.rate_ranges[self.NowMode()]
        print("機率區間：", rate_range)

        for i in range(3):
            for j in range(6):
                if RandNums[i] <= rate_range[j]:
                    self.Ps[i] = P.Dict[list(P.Dict.keys())[j]]
                    break

        #增加咖波累積數
        for p in self.Ps:
            if p.code == "A" and self.GssNum < 20 :
                self.GssNum += 1
        print(f"咖波累積數：{self.GssNum}")

    def Result(self):
        """結果"""
        super().Result()
        self.index_plus()
#endregion

if __name__ == "__main__":
    Game = PlayLaBaG()
    while Game.GameRunning():
        while True:
            if input("請按下ENTER") == "":
                break
        Game.Logic()
    Game.GameOver()
        