from random import randint
from src.element import Gss, Hhh, Hentai, Handsun, Kachu, Rrr

class P:
    def __init__(self, code: str = None, score_list: list[int] = None, rate_dict: dict[str, int]= 0, pic = None):
        self.code = code
        self.score_list = score_list
        self.rate_dict = rate_dict or {"Normal": 0}
        self.picture = pic

    def __str__(self):
        return self.code

        
class LaBaG:
    def __init__(self):
        self.name = "" #玩家名稱

        # 遊戲邏輯變數
        self.times = 30 #可遊玩次數 正常30
        self.played = 0 #已遊玩次數

        self.score = 0
        self.margin_score= 0

        self.history_score = 0

        self.P_dict = {
            "Gss":P("A",[625, 350, 150], {
                "Normal": 36,
                "SuperHHH": 19,
                "GreenWei": 36,
                "PiKaChu": 36
            }, Gss),
            "Hhh":P("B",[1250, 650, 220], {
                "Normal": 24,
                "SuperHHH": 5,
                "GreenWei": 24,
                "PiKaChu": 24
            }, Hhh),
            "Hentai":P("C",[2100, 1080, 380], {
                "Normal": 17,
                "SuperHHH": 19,
                "GreenWei": 17,
                "PiKaChu": 17
            }, Hentai),
            "Handsun":P("D",[2500, 1250, 420], {
                "Normal": 12,
                "SuperHHH": 19,
                "GreenWei": 12,
                "PiKaChu": 12
            }, Handsun),
            "Kachu":P("E",[10000, 5000, 1250], {
                "Normal": 8,
                "SuperHHH": 19,
                "GreenWei": 8,
                "PiKaChu": 8
            }, Kachu),
            "Rrr":P("F",[20000, 10000, 2500], {
                "Normal": 3,
                "SuperHHH": 19,
                "GreenWei": 3,
                "PiKaChu": 3
            }, Rrr),
        }

        #加分倍數
        self.score_times_dict = {
            "Normal": 1,
            "SuperHHH": 1,
            "GreenWei": 3,
            "PiKaChu": 1
        }
        self.score_time = 1 #本次加分倍數

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
        self.double_score = 0

        self.GreenWei = False
        self.GreenTimes = 0
        self.gss_times = 0

        self.PiKaChu = False
        self.kachu_times = 0

    def Logic(self):
        """邏輯流程"""
        self.ModtoScreen = False
        self.margin_score = 0
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
        print(f"P隨機數為：{RandNums[0]} | {RandNums[1]} | {RandNums[2]}")
        def acc_rate():
            res = list()
            acc = 0
            for i in self.P_dict:
                acc += self.P_dict[i].rate_dict[self.now_mod()]
                res.append(acc)
            return res
        
        rate_range = acc_rate()
        print("機率區間：", rate_range)

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

        self.score_time = self.score_times_dict[self.now_mod()]
        self.margin_score *= self.score_time
        print(f"加分倍數: {self.score_time}")
        

    def result(self):
        """結果"""
        self.played += 1
        self.score += self.margin_score
        print(f"")
        print(f' | {self.Ps[0]} | {self.Ps[1]} | {self.Ps[2]} |')
        print(f"+{self.margin_score}")
        print(f"目前分數：{self.score}")
        print(f"剩餘次數：{self.times - self.played}")
        

    def GameOver(self):
        """遊戲結束"""
        print("")
        print(f"遊戲已結束，最終分數為：{self.score}。")
        if self.score > self.history_score:
            self.history_score = self.score

    #region 超級阿禾模式(SuperHHH)
    def SuperFalse(self):
        self.SuperHHH = False
    
    def SuperRandom(self):
        self.SuperNum = randint(1, 100) #隨機數
        print(f"超級阿禾隨機數為: {self.SuperNum}")

    def judge_super(self):
        """判斷超級阿禾"""
        if not self.GameRunning:
            self.SuperFalse()
            return
        
        self.SuperRandom()
        self.double_score  = 0
        match self.now_mod():
            case "SuperHHH":
                self.SuperTimes -= 1
                print(f"超級阿禾剩餘次數:{self.SuperTimes}次")

                if all(p.code == "B" for p in self.Ps):
                    self.SuperTimes += 2
                    print("全阿禾，次數不消耗且+1！")
                if self.SuperTimes <= 0 : #超級阿禾次數用完
                    self.SuperFalse()

                    self.ModtoScreen = True

            case "Normal" | "PiKaChu":
                
                hhh_appear = any(p.code == "B" for p in self.Ps) #判斷是否有出現阿和
                if self.SuperNum <= self.SuperRate and hhh_appear:
                    self.SuperHHH = True
                    self.SuperTimes += 6
                    print(f"超級阿禾出現")
                    if self.PiKaChu:
                        self.KachuFalse()

                    self.ModtoScreen = True

                    #超級阿禾加倍
                    if all(p.code == "B" for p in self.Ps):
                        self.double_score = int(round(self.score / 2))
                        self.double_score *= self.score_time
                        self.margin_score += self.double_score
                        if self.score_time == 3:
                            print(f"(超級阿禾 x 綠光阿瑋加倍分:{self.double_score})")
                        else:
                            print(f"(超級阿禾加倍分:{self.double_score})")
            
    #endregion

    #region 綠光阿瑋模式(GreenWei)
    def GreenFalse(self):
        self.GreenWei = False
    
    def GreenRandom(self):
        self.GreenNum = randint(1, 100) #隨機數
        print(f"綠光阿瑋隨機數為: {self.GreenNum}")

    def judge_green(self):
        """判斷綠光阿瑋"""
        if not self.GameRunning():
            self.GreenFalse()
            return
        
        #增加咖波累積數
        for p in self.Ps:
            if p.code == "A" and self.gss_times < 20 :
                self.gss_times += 1
        print(f"咖波累積數：{self.gss_times}")

        self.GreenRandom()
        match self.now_mod():
            case "GreenWei":
                self.GreenTimes -= 1
                print(f"綠光阿瑋剩餘次數:{self.GreenTimes}次")
                if all(p.code == "A" for p in self.Ps):
                    self.GreenTimes += 1
                    print("全咖波，次數不消耗！")
                if self.GreenTimes <= 0 : #綠光阿瑋次數用完
                    self.GreenFalse()
                    self.judge_super()

                    self.ModtoScreen = True

            case "Normal" | "PiKaChu":
    
                gss_all = all(p.code == "A" for p in self.Ps) #判斷是否有出現並全部咖波
                if self.GreenNum <= self.GreenRate and gss_all :
                    self.GreenWei = True
                    self.GreenTimes += 2
                    print(f"綠光阿瑋出現")
                    if self.PiKaChu:
                        self.KachuFalse()
                    
                    self.ModtoScreen = True

                elif self.gss_times >= 20 : #咖波累積數達到20
                    self.GreenWei = True
                    self.GreenTimes += 2
                    print(f"綠光阿瑋出現")
                    self.gss_times = 0
                    if self.PiKaChu:
                        self.KachuFalse()
                    
                    self.ModtoScreen = True

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
            print(f"皮卡丘為你充電")
            print(f"已觸發 {self.kachu_times} 次皮卡丘充電")
            #關掉其他模式
            self.SuperFalse()
            self.GreenFalse()

            self.ModtoScreen = True
        else:
            self.PiKaChu = False
    #endregion
        
import json
class JsonLaBaG(LaBaG):
    """與json檔案連接的啦八機"""
    def __init__(self):
        super().__init__()
        self.json_data = None
        self.BeginAble = True # 用於每次的模擬
        self.index = "1" # 第 n 次的索引
        
        self.simulation = False # 用於中斷&開始模擬

    def reset(self):
        """重置"""
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

    def random(self):
        """遊戲變數隨機產生"""
        RandNums = [self.json_data[self.index]["RandNums[0]"], self.json_data[self.index]["RandNums[1]"], self.json_data[self.index]["RandNums[2]"]]
        print(f"P隨機數為：{RandNums[0]} | {RandNums[1]} | {RandNums[2]}")
        def acc_rate():
            res = list()
            acc = 0
            for i in self.P_dict:
                acc += self.P_dict[i].rate_dict[self.now_mod()]
                res.append(acc)
            return res
        
        rate_range = acc_rate()
        print("機率區間：", rate_range)

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

    def result(self):
        """結果"""
        self.index_plus()
        self.played += 1
        self.score += self.margin_score
        print(f"")
        print(f' | {self.Ps[0]} | {self.Ps[1]} | {self.Ps[2]} |')
        print(f"+{self.margin_score}")
        print(f"目前分數：{self.score}")
        print(f"剩餘次數：{self.times - self.played}")

    
    def SuperRandom(self):
        self.SuperNum = self.json_data[self.index]["SuperHHH"]
        print(f"超級阿禾隨機數為: {self.SuperNum}")

    def GreenRandom(self):
        self.GreenNum = self.json_data[self.index]["GreenWei"]
        print(f"綠光阿瑋隨機數為: {self.GreenNum}")


     

            