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
        super().JudgeMode()
        now_mode = self.NowMode()
        match now_mode:
            case "SuperHHH":
                if self.ModtoScreen:
                    print(f"超級阿禾出現")
                    if self.double_score != 0:
                            print(f"(超級阿禾加倍分:{self.double_score})")
                else:
                    if all(p.code == "B" for p in self.Ps):
                        print("全阿禾，次數不消耗且+1！")
                print(f"超級阿禾剩餘次數:{self.SuperTimes}次")
            case "GreenWei":
                if self.ModtoScreen:
                    print(f"綠光阿瑋出現")
                else:
                    if all(p.code == "A" for p in self.Ps):
                        print("全咖波，次數不消耗！")
                print(f"綠光阿瑋剩餘次數:{self.GreenTimes}次")
                
            case "PiKaChu":
                if self.ModtoScreen:
                    print(f"皮卡丘為你充電")
                    print(f"已觸發 {self.kachu_times} 次皮卡丘充電")

    def GameOver(self):
        """遊戲結束"""
        print("")
        print(f"遊戲已結束，最終分數為：{self.score}。")
        if self.score > self.history_score:
            self.history_score = self.score

#region JsonLaBaG
import json
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
        