#目標分數
from random import randint
import math
from src.Sheet import Sheet
from src.LaBaG import LaBaG

class TargetLaBaG(LaBaG):
    def __init__(self):
        super().__init__()
        delattr(self, "kachu_times")
        self.superS = 0
        self.greenS = 0
        self.kachuS = 0
                    
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
                self.kachuS += 1
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
                    self.superS += 1
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
                    self.greenS += 1
                    if self.PiKaChu:
                        self.PiKaChu = False
                    
                    self.ModtoScreen = True
                    return

                elif self.GssNum >= 20 : #咖波累積數達到20
                    self.GreenWei = True
                    self.GreenTimes += 2
                    self.greenS += 1
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
            
while True:   
    try:
        target = int (input("請輸入目標分數"))
        if target > 0:
            break
        else:
            print("目標分數必須大於 0")
    except ValueError as e:
        print(f"請輸入有效的數字: {e}")

Game = TargetLaBaG()

recent_max = 0

i = 0
while True :
    i += 1
    if i < 10 :
        LOG = 2
    else:
        LOG = int (round(math.log10(i)) + 2)
    Game.Logic()

    print(f"第{i : {LOG}}次 分數：{Game.score : 8} ({Game.superS : 2} 次 超級阿禾 )({Game.greenS : 2} 次 綠光阿瑋 )({Game.kachuS : 2} 次  皮卡丘充電)【目前最大值：{recent_max}】")
    # 檢查是否達到目標
    if Game.score >= target:
        break  # 如果達到目標，則退出迴圈
    elif Game.score > recent_max:
        recent_max = Game.score
        if recent_max >= 1000000:
            Sheet.CommitScore('模擬測試最高分', recent_max)
        
print (f"第{i: {LOG}}次達成：{Game.score : 8} ({Game.superS : 2} 次 超級阿禾 )({Game.greenS : 2} 次 綠光阿瑋 )({Game.kachuS : 2} 次  皮卡丘充電)")  


