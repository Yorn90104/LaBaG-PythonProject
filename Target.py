#目標
 
import sys , math
sys.stdout.reconfigure(encoding='utf-8')

from random import randint #隨機數字

import subprocess
def commit_score(name, score):
    """上傳資料至試算表"""
    if name != "" :
        url = f"https://docs.google.com/forms/d/18dVGtPExBUc0p1VbsmMxCyujQoldI6GKQWZQGJQ-yzY/formResponse?entry.582969025={name}&entry.995493130={score}"
        subprocess.Popen(['curl', url], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("資料已上傳")
    else:
        print("名稱為空，資料未上傳！")

i_data = {}
recent_max = 0



def game(i, LOG):
        #region 定義區
        global recent_max

        #初始設定
        game_running = True

        ram1 , ram2 , ram3 = 0 , 0 , 0
        SuperRam = 0
        GreenRam = 0

        p1 , p2 , p3 = '' , '' , ''
        all_p = []

        score = 0
        add = 0
        times = 30
        ed = 0

        SuperTimes = 0
        SuperHHH = False
        SuperFirst = False
        superS = 0

        GreenTimes = 0
        GreenWei = False
        GreenFirst = False
        gss_times = 0
        greenS = 0

        PiKaChu = False
        kachuS = 0

        #機率
        def acc_rate(original_rate):
                result_rate= []
                acc = 0
                for x in original_rate:
                    acc += x
                    result_rate.append(acc)
                return result_rate

        normal_acc = acc_rate([36, 24, 17, 12, 8, 3])

        super_acc = acc_rate([19, 5, 19, 19, 19, 19])

        #分數清單
        same3 = [625, 1250, 2100, 2500, 10000, 20000]
        same2 = [350, 650, 1080, 1250, 5000, 10000]
        same1 = [150, 220, 380, 420, 1250, 2500]

        #endregion
        
        #region 普通函式區
        def change_rate(rate, y):
                """根據隨機數和機率找歸屬 (隨機數)"""
                if y <= rate[0] :
                    return 'A'
                elif y <= rate[1] :
                    return 'B'
                elif y <= rate[2] :
                    return 'C'
                elif y <= rate[3] :
                    return 'D'
                elif y <= rate[4] :
                    return 'E'
                elif y <= rate[5] :
                    return 'F'


        def ADD(x,y,lst) :
                '(歸屬,增加分,分數清單)'
                if x == 'A':
                    y = y + lst[0]
                elif x == 'B' :
                    y = y + lst[1]
                elif x == 'C' :
                    y = y + lst[2]
                elif x == 'D' :
                    y = y + lst[3]
                elif x == 'E' :
                    y = y + lst[4]
                elif x == 'F' :
                    y = y + lst[5]
                return y

        def calculate_score(p1 , p2 , p3 , a):
                """計算分數"""
                #3個相同
                if p1 == p2 == p3 :
                    a = ADD(p1 , a , same3)

                #2個相同=(2個相同的+1個不同的)/1.3
                # 1 & 2
                elif p1 == p2 :
                    a = ADD(p1 , a , same2)
                    #不同的
                    a = ADD(p3 , a , same1)

                    a = round( a / 1.3 )

                # 2 & 3
                elif p2 == p3 :
                    #2個同
                    a = ADD(p2 , a , same2)
                    #不同的
                    a = ADD(p1 , a , same1)

                    a = round( a / 1.3 )

                # 1 & 3
                elif p1 == p3 :
                    #2個同
                    a = ADD(p3 , a , same2)
                    #不同的
                    a = ADD(p2 , a , same1)

                    a = round( a / 1.3 )

                #3個都不同 加總/3
                elif p1 != p2 != p3 :
                    #1
                    a = ADD(p1 , a , same1)
                    
                    #2
                    a = ADD(p2 , a , same1)
                    
                    #3
                    a = ADD(p3 , a , same1)

                    a = round( a / 3 )
                return a

        def result() :
                nonlocal score , add , ed , p1 , p2 , p3
                ed += 1
                score += add
                add = 0
                #endregion

        def now_mod(): #現在模式
                nonlocal SuperHHH, GreenWei, PiKaChu
                mod = ""
                if SuperHHH :
                    mod = "SuperHHH"
                elif GreenWei :
                    mod = "GreenWei"
                elif PiKaChu :
                    mod = "PiKaChu"
                else :
                    mod = "Normal"
                
                return mod

        #region 超級阿禾區
        def super_times(Times) :
                nonlocal SuperHHH, SuperFirst
                if SuperHHH :
                    SuperFirst = False
                    Times -= 1
                return Times

        def super_ram(SuperRam):
                """阿禾隨機數"""
                SuperRam = randint(1,100)
                return SuperRam

        def judge_super(all_p, game_running = True, ModEnd = False):
                """判斷超級阿禾"""
                nonlocal SuperRam, SuperHHH, SuperTimes, SuperFirst, superS
                if not game_running :
                    SuperHHH = False
                    return
                
                mod = now_mod()
                if mod == "SuperHHH" : #正處於超級阿禾狀態
                    if all(x == "B" for x in all_p):
                            SuperTimes += 2
                    if SuperTimes <= 0 : #超級阿禾次數用完
                            SuperHHH = False
                            judge_super(all_p, ModEnd = True)
                elif mod == "Normal" or mod == "PiKaChu" or ModEnd : #未處於超級阿禾狀態
                    hhh_appear = False
                    #判斷是否有出現阿和
                    if any(x == "B" for x in all_p):
                            hhh_appear = True
                    if SuperRam <= 15 and hhh_appear :#超級阿禾出現的機率
                            SuperHHH = True
                            SuperFirst = True
                            superS += 1
                            SuperTimes = 6
                            KachuFalse()
                


        def switch_rate(normal_acc):
                nonlocal super_acc
                mod = now_mod()
                if mod == "SuperHHH" :
                    return super_acc
                elif mod == "Normal" or mod == "GreenWei" or mod == "PiKaChu" :
                    return normal_acc
        
        def super_double(all_SB, score, add):
                """超級阿禾加倍 獲得當前分數0.5倍的分數"""
                if all_SB :
                    double_score = int(round(score / 2))
                    add += double_score
                    return add

        def three_super(all_p, score, add):
                nonlocal SuperHHH, SuperTimes, SuperFirst
                """"檢查是否三個超級阿禾"""
                if all(p == "B" for p in all_p) and SuperHHH and SuperFirst:
                    all_SB = True
                    add = super_double(all_SB, score, add)
                    return add
                else:
                    return add
                #endregion

        #region 綠光阿瑋區
        def green_times(Times) :
                nonlocal GreenWei, GreenFirst
                if GreenWei :
                    GreenFirst = False
                    Times -= 1
                return Times

        def green_ram(GreenRam):
                """阿瑋隨機數"""
                GreenRam = randint(1,100)
                return GreenRam

        def gss_acc_times(all_p):
                """增加咖波累積數"""
                nonlocal gss_times
                if any(p == "A" for p in all_p) :
                    for i in range(0,len(all_p)):
                            if all_p[i] == "A" and gss_times < 20 :
                                gss_times += 1

        def judge_green(all_p, game_running = True, Kachu = False):
                """判斷綠光阿瑋"""
                nonlocal GreenRam, GreenWei, GreenTimes, GreenFirst, gss_times, greenS
                if not game_running :
                    GreenWei = False
                    if Kachu == False:
                            gss_times = 0
                    return
                
                mod = now_mod()
                gss_acc_times(all_p)
                if mod == "GreenWei" : 
                    if all(x == "A" for x in all_p):
                            GreenTimes += 1
                    if GreenTimes <= 0 : 
                            GreenWei = False
                            judge_super(all_p, ModEnd = True)
                elif mod == "Normal" or mod == "PiKaChu"  : 
                    gss_all = False

                    if all(x == "A" for x in all_p):
                            gss_all = True
                    if GreenRam <= 35 and gss_all :#超級阿禾出現的機率
                            GreenWei = True
                            GreenFirst = True
                            greenS += 1
                            GreenTimes = 2
                            KachuFalse()

                    elif gss_times >= 20 : #咖波累積數達到20
                            GreenWei = True
                            GreenFirst = True
                            greenS += 1
                            GreenTimes = 2
                            gss_times = 0
                            KachuFalse()
                
        def switch_times():
                """加分倍數"""
                mod = now_mod()
                if mod == "GreenWei" :#綠光阿瑋使得分增加2倍(*3)
                    t = 3
                elif mod == "Normal" or mod == "SuperHHH" or mod == "PiKaChu" :
                    t = 1
                return t
        #endregion

        #region 皮卡丘充電區
        def KachuFalse():
                """關掉皮卡丘"""
                nonlocal PiKaChu
                PiKaChu = False

        def judge_kachu(all_p, times, ed,  game_running = True):
                """判斷皮卡丘"""
                nonlocal PiKaChu, kachuS
                if not game_running:
                    PiKaChu = False
                    return
                #遊戲進行
                if ed + 1 >= times:
                    kachu_appear = False
                    if any(p == "E" for p in all_p) :
                            kachu_appear = True
                    if kachu_appear:
                            PiKaChu = True
                            ed -= 5
                            kachuS += 1
                            #關掉其他模式
                            judge_super(all_p, False)
                            judge_green(all_p, False, True)     
                return ed
        
        #endregion

        #遊戲運作區
        while ed < times :
                SuperTimes = super_times(SuperTimes)
                GreenTimes = green_times(GreenTimes)

                #隨機數
                ram1 , ram2 , ram3 = randint(1,100) , randint(1,100) , randint(1,100)
                SuperRam = super_ram(SuperRam)
                GreenRam = green_ram(GreenRam)

                #歸屬
                use_rate = switch_rate(normal_acc)
                p1 = change_rate(use_rate,ram1)
                p2 = change_rate(use_rate,ram2)
                p3 = change_rate(use_rate,ram3)
                
                all_p = [p1, p2, p3]
                judge_super(all_p)

                #增加分數
                use_times = switch_times()
                judge_green(all_p)
                add = calculate_score(p1 , p2 , p3 , add)
                add = three_super(all_p, score, add)
                add *= use_times

                result()
                #遊戲繼續
                ed = judge_kachu(all_p, times, ed)
                
        #遊戲結束
        game_running = False
        judge_super(all_p, game_running)
        judge_green(all_p, game_running)
        judge_kachu(all_p, times, ed, game_running)
        
        
        if score > recent_max:
            recent_max = score
            if recent_max >= 950000:
             commit_score('模擬測試最高分', recent_max)
        print(f"第{i : {LOG}}次 分數：{score : 8} ({superS : 2} 次 超級阿禾 )({greenS : 2} 次 綠光阿瑋 )({kachuS : 2} 次  皮卡丘充電)【目前最大值：{recent_max}】")
        return [score, superS, greenS, kachuS]
    

target = int (input("請輸入目標分數"))


i = 0
while True :
    i += 1
    if i < 10 :
        LOG = 2
    else:
        LOG = int (round(math.log10(i)) + 2)

    i_data = game (i, LOG)

    # 檢查(列表)的第一個索引值是否達到目標
    if i_data[0] >= target:
        break  # 如果達到目標，則退出迴圈
    

 
print (f"第{i: {LOG}}次達成： {i_data[0]} ({i_data[1] : 2} 次超級阿禾 )({i_data[2] : 2} 次綠光阿瑋 )({i_data[3] : 2} 次  皮卡丘充電)")  


