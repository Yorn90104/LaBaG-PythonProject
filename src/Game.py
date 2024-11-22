from random import randint
from src.GUI import (
                        update_picture, switch_frame, image_button, delete_button,
                        play_music , stop_music, play_sound, switch_music
                        )
from src.Element import (
                            QST, BG, Title, 
                            gss , hhh , hentai , handsun , kachu , rrr,
                            super_hhh, SuperPOP, SuperBG, SuperQST, SuperTitle,
                            green_wei, GreenPOP, GreenBG, GreenQST, GreenTitle, GreenLeft, GreenMid, GreenRight, 
                            pikachu, KachuPOP, KachuBG, KachuQST, KachuTitle,
                            Ding, SuperUP, GreenUP,
                            bgm, SuperMusic, GreenMusic, KachuMusic
                            )
from src.Sheet import find_history_score, commit_score

class Game:

    def __init__(self):
        self.name = "" #玩家名稱

        # 遊戲邏輯變數
        self.times = 30 #可遊玩次數 正常30
        self.ed = 0 #已遊玩次數

        self.score = 0
        self.add= 0
        self.history_score = 0

        #遊戲後臺變數
        self.ram1, self.ram2, self.ram3 = 0, 0, 0
        self.p1, self.p2, self.p3 = '', '', ''
        self.all_p = []

        #分數清單(A, B, C, D, E, F)
        self.same3 = [625, 1250, 2100, 2500, 10000, 20000]
        self.same2 = [350, 650, 1080, 1250, 5000, 10000]
        self.same1 = [150, 220, 380, 420, 1250, 2500]
        #機率
        self.rate_dict = dict(
                            Normal = [36, 24, 17, 12, 8, 3],
                            SuperHHH = [19, 5, 19, 19, 19, 19], 
                            GreenWei = [36, 24, 17, 12, 8, 3],
                            PiKaChu = [36, 24, 17, 12, 8, 3]
                            )
        #加分倍數
        self.times_dict = dict(
                            Normal = 1,
                            SuperHHH = 1,
                            GreenWei = 3,
                            PiKaChu = 1
                            )

        #圖片清單(A, B, C, D, E, F)
        self.picture_list = [gss , hhh , hentai , handsun , kachu , rrr]

        #region 特殊模式
        #超級阿禾
        self.SuperRate = 15
        self.SuperHHH = False
        self.SuperRam = 0
        self.SuperTimes = 0

        #綠光阿瑋
        self.GreenRate = 35
        self.GreenWei = False
        self.GreenRam = 0
        self.GreenTimes = 0
        self.gss_times = 0

        #皮卡丘
        self.PiKaChu = False
        self.kachu_times = 0

        #endregion

        #音樂判斷
        self.bgm_playing = False
        
    #region 內部運算
    def now_mod(self):
        if self.SuperHHH:
            return "SuperHHH"
        elif self.GreenWei:
            return "GreenWei"
        elif self.PiKaChu:
            return "PiKaChu"
        else:
            return "Normal"

    def game_start_reset(self, canvas_Game, name = ""):
        """遊戲開始。恢復預設設置"""
        self.name = name
        self.history_score = find_history_score(self.name)
        self.ed = 0
        self.score = 0
        self.add= 0

        self.ram1, self.ram2, self.ram3 = 0, 0, 0
        self.p1, self.p2, self.p3 = '', '', ''
        self.all_p = []

        self.reset_item(canvas_Game)
    
    def random_value(self):
        """隨機數值"""
        self.ram1, self.ram2, self.ram3 = randint(1,100), randint(1,100), randint(1,100)
        print(f"圖片隨機數為：{self.ram1} | {self.ram2} | {self.ram3}")

    def classify_p(self, ram):
        """隨機數根據機率區間歸類(隨機數, 使用機率)"""
        def acc_rate(original_rate):
            """累加機率"""
            result_rate= []
            acc = 0
            for x in original_rate:
                acc += x
                result_rate.append(acc)
            return result_rate

        acc = acc_rate(self.rate_dict[self.now_mod()])
        print(f"機率區間為：{acc}")

        if ram <= acc[0] :
            return 'A'
        elif ram <= acc[1] :
            return 'B'
        elif ram <= acc[2] :
            return 'C'
        elif ram <= acc[3] :
            return 'D'
        elif ram <= acc[4] :
            return 'E'
        elif ram <= acc[5] :
            return 'F'
        
    def calculate_score(self):
        """計算分數"""

        def margin_score (r, add, lst):
            """邊際分數 (歸屬, 增加分數, 分數清單)"""
            if r == 'A':
                add += lst[0]
            elif r == 'B':
                add += lst[1]
            elif r == 'C':
                add += lst[2]
            elif r == 'D':
                add += lst[3]
            elif r == 'E':
                add += lst[4]
            elif r == 'F':
                add += lst[5]
            return add
        
        self.add = 0
        #3個相同
        if self.p1 == self.p2 == self.p3 :
            self.add = margin_score(self.p1 , self.add , self.same3)

        #2個相同=(2個相同的+1個不同的)/1.3
        # 1 & 2
        elif self.p1 == self.p2 :
            self.add = margin_score(self.p1 , self.add , self.same2)
            #不同的
            self.add = margin_score(self.p3 , self.add , self.same1)

            self.add = round( self.add / 1.3 )

        # 2 & 3
        elif self.p2 == self.p3 :
            #2個同
            self.add = margin_score(self.p2 , self.add , self.same2)
            #不同的
            self.add = margin_score(self.p1 , self.add , self.same1)

            self.add = round( self.add / 1.3 )

        # 1 & 3
        elif self.p1 == self.p3 :
            #2個同
            self.add = margin_score(self.p3 , self.add , self.same2)
            #不同的
            self.add = margin_score(self.p2 , self.add , self.same1)

            self.add = round( self.add / 1.3 )

        #3個都不同 加總/3
        elif self.p1 != self.p2 != self.p3 :
            #1
            self.add = margin_score(self.p1 , self.add , self.same1)
            
            #2
            self.add = margin_score(self.p2 , self.add , self.same1)
            
            #3
            self.add = margin_score(self.p3 , self.add , self.same1)

            self.add = round( self.add / 3 )

    def result(self):
        """結果"""
        self.ed += 1
        self.score += self.add
        print(f"")
        print(f' | {self.all_p[0]} | {self.all_p[1]} | {self.all_p[2]} |')
        print(f"+{self.add}")
        print(f"目前分數：{self.score}")
        print(f"剩餘次數：{self.times - self.ed}")
     
    def game_over(self):
        """遊戲結束"""
        print("")
        print(f"遊戲已結束，最終分數為：{self.score}。")
        if self.score > self.history_score:
            self.history_score = self.score
        commit_score(self.name, self.score)
            
    #endregion

    #region 外部表現

    def bgm_on_off(self, button_music, game_running = True) :
        """音樂開關"""
        mod = self.now_mod()
        if mod == "SuperHHH":
            file = SuperMusic
        elif mod == "GreenWei":
            file = GreenMusic
        elif mod == "PiKaChu":
            file = KachuMusic
        else:
            file = bgm
        
        #關
        if self.bgm_playing or game_running == False :
            stop_music()
            button_music.config(text="關", bg="#C0C0C0") 
            print("BGM已停止")
            self.bgm_playing = False
        #開
        else :
            play_music(file) 
            button_music.config(text="開", bg="#00FF00")
            print("BGM已開啟")
            self.bgm_playing = True

    def reset_item(self, canvas_Game):
        self.SuperFalse()
        self.GreenFalse(canvas_Game)
        self.KachuFalse(canvas_Game)

        update_picture(canvas_Game , "LP" , QST)
        update_picture(canvas_Game , "MP" , QST)
        update_picture(canvas_Game , "RP" , QST)

        canvas_Game.itemconfig("BG", image = BG)
        canvas_Game.itemconfig("Title", image = Title)
        canvas_Game.itemconfig("Add", text=f"")
        canvas_Game.itemconfig("Score", text= f"目前分數：{self.score}")
        canvas_Game.itemconfig("Times", text= f"剩餘次數：{self.times - self.ed}")
        canvas_Game.itemconfig("history_score", text= f"歷史最高分數：{self.history_score}")
        canvas_Game.itemconfig("mod_1", text = f"")
        canvas_Game.itemconfig("mod_2", text = f"")
        canvas_Game.itemconfig("gss", text = f"咖波累積數：{self.gss_times}")

    def normal_init(self, canvas_Game):
        
        update_picture(canvas_Game , "LP" , QST)
        update_picture(canvas_Game , "MP" , QST)
        update_picture(canvas_Game , "RP" , QST)

        canvas_Game.itemconfig("Add", text=f"")
        canvas_Game.itemconfig("Score", text= f"目前分數：{self.score}")
        canvas_Game.itemconfig("Times", text= f"剩餘次數：{self.times - self.ed}")
        canvas_Game.itemconfig("mod_2", text = f"")

    def change_picture(self ,canvas_Game,  tag , p):
        """變換圖片 (畫面, 標籤, p)"""

        def PrizePIC(p):
            """根據歸類選擇圖 (p)"""
            if p == "A":
                return self.picture_list[0]
            elif p == "B":
                return self.picture_list[1]
            elif p == "C":
                return self.picture_list[2]
            elif p == "D":
                return self.picture_list[3]
            elif p == "E":
                return self.picture_list[4]
            elif p == "F":
                return self.picture_list[5]
            
        new_pic = PrizePIC(p)
        update_picture(canvas_Game, tag , new_pic)
        play_sound(Ding)

    def result_txt(self, canvas_Game):
        """顯示結果文字"""
        canvas_Game.itemconfig("Add", text= f"+{self.add}")
        canvas_Game.itemconfig("Score", text= f"目前分數：{self.score}")
        canvas_Game.itemconfig("Times", text= f"剩餘次數：{self.times - self.ed}")

    def to_end_frame(self,canvas_End, frame_Game, frame_End, button_music):
        """結算畫面"""
        switch_frame(frame_Game, frame_End)
        self.bgm_on_off(button_music, False)
        play_sound(Ding)
        print("切換結束畫面")
        canvas_End.itemconfig("Name", text =  f"{self.name}")
        canvas_End.itemconfig("over", text="遊戲結束！") 
        canvas_End.itemconfig("final_score", text=f"最終分數：{self.score}")  # 最終分數顯示
        canvas_End.itemconfig("HS", text= f"歷史最高分數：{self.history_score}")
        
    #region 超級阿禾模式(SuperHHH)
    def SuperFalse(self):
        self.SuperHHH = False

    def super_ram(self):
        """阿禾隨機數"""
        self.SuperRam = randint(1,100)
        print(f"超級阿禾隨機數為：{self.SuperRam}")

    def super_times(self, canvas_Game) :
        if self.SuperHHH :
            self.SuperTimes -= 1
            print(f"超級阿禾剩餘次數:{self.SuperTimes}次")
            canvas_Game.itemconfig("mod_1", text = f"超級阿禾剩餘次數:{self.SuperTimes}次", fill = "#FF00FF")

    def judge_super(self, win, canvas_Game, game_running = True, ModEnd = False):
        """判斷超級阿禾"""
        if not game_running :
                self.SuperHHH = False
                win.after(2000 , lambda : self.super_screen(win,canvas_Game, False))
                return
        #遊戲進行
        mod = self.now_mod()
        if mod == "SuperHHH" : #正處於超級阿禾模式
            if all(p == "B" for p in self.all_p): #超級阿禾次數未用完且全阿禾
                self.SuperTimes += 2
                print("全阿禾，次數不消耗且+1！")
            if self.SuperTimes <= 0 : #超級阿禾次數用完
                self.SuperHHH = False
                win.after(2000 , lambda : self.super_screen(win,canvas_Game))

        elif mod == "Normal" or mod == "PiKaChu" or ModEnd: #未處於任何模式 or 皮卡丘模式 or 在其他模式結尾
            hhh_appear = False
            #判斷是否有出現阿和
            if any(x == "B" for x in self.all_p):
                hhh_appear = True

            if self.SuperRam <= self.SuperRate and hhh_appear :#超級阿禾出現的機率
                self.SuperHHH = True
                self.SuperTimes = 6
                win.after(2800 , lambda : self.change_hhh(canvas_Game))
                win.after(3500 , lambda : self.super_screen(win, canvas_Game))
                self.KachuFalse(canvas_Game)

                if all( b == "B" for b in self.all_p):
                    """超級阿禾加倍"""
                    double_score = int(round(self.score / 2))
                    self.add += double_score
                    if self.rate_dict[self.now_mod()] == 3:
                        print(f"(超級阿禾x綠光阿瑋加倍分:{double_score * 3})")
                        win.after(3000,lambda : canvas_Game.itemconfig("mod_2", text = f"(超級阿禾x綠光阿瑋加倍分:{double_score * 3})", fill = "yellow"))
                    else:
                        print(f"(超級阿禾加倍分:{double_score})")
                        win.after(3000,lambda : canvas_Game.itemconfig("mod_2", text = f"(超級阿禾加倍分:{double_score})", fill = "yellow"))
        
    def change_hhh(self, canvas_Game):
        """把普通阿禾變成超級阿禾"""
        if self.all_p[0] == "B":
            self.all_p[0] = "SB"
            canvas_Game.itemconfig("LP" , image = super_hhh)
        if self.all_p[1] == "B":
            self.all_p[1] = "SB"
            canvas_Game.itemconfig("MP" , image = super_hhh)
        if self.all_p[2] == "B":
            self.all_p[2] = "SB"
            canvas_Game.itemconfig("RP" , image = super_hhh)
        play_sound(SuperUP)

    def super_screen(self, win, canvas_Game, game_running = True):
        """超級阿禾版面"""
        if self.SuperHHH :
            super_pop = image_button(win, lambda: delete_button(super_pop), canvas_Game, SuperPOP, 225 , 400, "flat", 0)
            print("超級阿禾出現了！")
            canvas_Game.itemconfig("BG", image = SuperBG)
            canvas_Game.itemconfig("Title", image = SuperTitle)
            canvas_Game.itemconfig("mod_1", text = f"超級阿禾剩餘次數:{self.SuperTimes}次", fill = "#FF00FF")
            switch_music(self.bgm_playing, SuperMusic)
            

        else :
            canvas_Game.itemconfig("BG", image = BG)
            canvas_Game.itemconfig("Title", image = Title)
            canvas_Game.itemconfig("mod_1", text = "")
            switch_music(self.bgm_playing, bgm, game_running)

    def Super_init(self, canvas_Game):
        
        update_picture(canvas_Game , "LP" , SuperQST)
        update_picture(canvas_Game , "MP" , SuperQST)
        update_picture(canvas_Game , "RP" , SuperQST)

        canvas_Game.itemconfig("Add", text=f"")
        canvas_Game.itemconfig("Score", text= f"目前分數：{self.score}")
        canvas_Game.itemconfig("Times", text= f"剩餘次數：{self.times - self.ed}")
        canvas_Game.itemconfig("mod_2", text = f"")

    #endregion
    
    #region 綠光阿瑋模式(GreenWei)
    def GreenFalse(self, canvas_Game):
        self.GreenWei = False
        self.gss_times = 0
        self.gss_txt(canvas_Game)

    def green_ram(self):
        """阿瑋隨機數"""
        self.GreenRam = randint(1,100)
        print(f"綠光阿瑋隨機數為：{self.GreenRam}")

    def green_times(self, canvas_Game) :
        if self.GreenWei :
            self.GreenTimes -= 1
            print(f"綠光阿瑋剩餘次數:{self.GreenTimes}次")
            canvas_Game.itemconfig("mod_1", text = f"綠光阿瑋剩餘次數:{self.GreenTimes}次", fill = "#00FF00")

    def gss_txt(self, canvas_Game):
        canvas_Game.itemconfig("gss", text = f"咖波累積數：{self.gss_times}")

    def gss_acc_times(self, win, canvas_Game):
        """增加咖波累積數"""
        if any(p == "A" for p in self.all_p) :
            for i in range(0,len(self.all_p)):
                if self.all_p[i] == "A" and self.gss_times < 20 :
                    self.gss_times += 1
        print(f"咖波累積數：{self.gss_times}")
        win.after(3000, lambda : self.gss_txt(canvas_Game))

    def judge_green(self, win, canvas_Game, game_running = True):
        """判斷綠光阿瑋"""
        if not game_running:
            self.GreenWei = False
            if self.PiKaChu == False: #不是進入皮卡丘模式
                self.gss_times = 0 #才把咖波累積數歸0
            win.after(2000 , lambda : self.green_screen(win, canvas_Game, False))
            return
        #遊戲進行
        mod = self.now_mod()
        self.gss_acc_times(win, canvas_Game)
        if mod == "GreenWei" : #處於綠光阿瑋模式
            if all(p == "A" for p in self.all_p) :#綠光次數未用完且全部咖波
                self.GreenTimes += 1
                canvas_Game.itemconfig("mod_1", text = f"綠光阿瑋剩餘次數:{self.GreenTimes}次", fill = "#00FF00")
                print("全咖波，次數不消耗！")
            if self.GreenTimes <= 0 : #綠光次數用完
                self.GreenWei = False
                win.after(2000 , lambda : self.green_screen(win, canvas_Game))
                self.judge_super(win, canvas_Game, ModEnd = True)
            
        elif mod == "Normal" or mod == "PiKaChu" : #未處於任何模式 or 皮卡丘模式
            gss_all = False

            #判斷是否有出現並全部咖波
            if all(x == "A" for x in self.all_p):
                gss_all = True

            if self.GreenRam <= self.GreenRate and gss_all : #3咖波
                self.GreenWei = True
                self.GreenTimes = 2
                win.after(3000, lambda : self.gss_txt(canvas_Game))
                win.after(2800 , lambda : self.change_gss(canvas_Game))
                win.after(3500 , lambda : self.green_screen(win, canvas_Game))
                self.KachuFalse(canvas_Game)

            elif self.gss_times >= 20 : #咖波累積數達到20
                self.GreenWei = True
                self.GreenTimes = 2
                self.gss_times = 0
                win.after(3000, lambda : self.gss_txt(canvas_Game))
                win.after(2800 , lambda : self.change_gss(canvas_Game, gss_all))
                win.after(3500 , lambda : self.green_screen(win, canvas_Game))
                self.KachuFalse(canvas_Game)

    def change_gss(self, canvas_Game, gss_all = True):
        """把咖波變成阿瑋"""
        if gss_all :
            self.all_p[0], self.all_p[1], self.all_p[2] = "GW", "GW", "GW"
            canvas_Game.itemconfig("LP" , image = GreenLeft)
            canvas_Game.itemconfig("MP" , image = GreenMid)
            canvas_Game.itemconfig("RP" , image = GreenRight)
        elif any(p == "A" for p in self.all_p):
            if self.all_p[0] == "A":
                self.all_p[0] = "GW"
                canvas_Game.itemconfig("LP" , image = green_wei)
            if self.all_p[1] == "A":
                self.all_p[1] = "GW"
                canvas_Game.itemconfig("MP" , image = green_wei)
            if self.all_p[2] == "A":
                self.all_p[2] = "GW"
                canvas_Game.itemconfig("RP" , image = green_wei)
        else :
            canvas_Game.itemconfig("LP" , image = green_wei)
            canvas_Game.itemconfig("MP" , image = green_wei)
            canvas_Game.itemconfig("RP" , image = green_wei)
        play_sound(GreenUP)

    def green_screen(self, win, canvas_Game, game_running = True):
        """綠光阿瑋版面"""
        if self.GreenWei :
            green_pop = image_button(win, lambda: delete_button(green_pop), canvas_Game, GreenPOP, 225 , 400, "flat", 0)
            print("綠光阿瑋出現了！")
            canvas_Game.itemconfig("BG", image = GreenBG)
            canvas_Game.itemconfig("Title", image = GreenTitle)
            canvas_Game.itemconfig("mod_1", text = f"綠光阿瑋剩餘次數:{self.GreenTimes}次", fill = "#00FF00")
            switch_music(self.bgm_playing, GreenMusic)
            

        else :
            canvas_Game.itemconfig("BG", image = BG)
            canvas_Game.itemconfig("Title", image = Title)
            canvas_Game.itemconfig("mod_1", text = "")
            switch_music(self.bgm_playing, bgm,game_running)

    def Green_init(self, canvas_Game):
        update_picture(canvas_Game , "LP" , GreenQST)
        update_picture(canvas_Game , "MP" , GreenQST)
        update_picture(canvas_Game , "RP" , GreenQST)

        canvas_Game.itemconfig("Add", text=f"")
        canvas_Game.itemconfig("Score", text= f"目前分數：{self.score}")
        canvas_Game.itemconfig("Times", text= f"剩餘次數：{self.times - self.ed}")
        canvas_Game.itemconfig("mod_2", text = f"")
    #endregion

    #region 皮卡丘充電區(PiKaChu)
    def KachuFalse(self, canvas_Game):
        """關掉皮卡丘"""
        self.PiKaChu = False
        canvas_Game.itemconfig("mod_1", text = f"")

    def kachu_time(self, canvas_Game):
        self.kachu_times += 1
        print(f"已觸發 {self.kachu_times} 次皮卡丘充電")
        canvas_Game.itemconfig("mod_1", text = f"已觸發 {self.kachu_times} 次皮卡丘充電", fill = "#FFFF00")

    def judge_kachu(self, win, canvas_Game,  game_running = True):
        """判斷皮卡丘"""
        if not game_running:
            self.PiKaChu = False
            win.after(2000 , lambda : self.kachu_screen(win, canvas_Game, False))
            self.kachu_times =0
            return
        #遊戲進行
        if self.ed + 1 >= self.times:
            kachu_appear = False
            if any(p == "E" for p in self.all_p) :
                kachu_appear = True
            if kachu_appear:
                self.PiKaChu = True
                self.ed -= 5
                #關掉其他模式
                self.judge_super(win, canvas_Game, False)
                self.judge_green(win, canvas_Game, False)
                win.after(2500 , lambda : self.change_kachu(canvas_Game))
                win.after(3500 , lambda : self.kachu_screen(win, canvas_Game))

                win.after(3500 , lambda : self.kachu_time(canvas_Game))

    def change_kachu(self, canvas_Game):
        """把皮卡丘變成皮卡丘"""
        switch_music(self.bgm_playing,KachuMusic)
        if self.all_p[0] == "E":
            canvas_Game.itemconfig("LP" , image = pikachu)
        if self.all_p[1] == "E":
            canvas_Game.itemconfig("MP" , image = pikachu)
        if self.all_p[2] == "E":
            canvas_Game.itemconfig("RP" , image = pikachu)

    def kachu_screen(self, win, canvas_Game, game_running = True):
        """皮卡丘版面"""
        if self.PiKaChu :
            kachu_pop = image_button(win, lambda: delete_button(kachu_pop), canvas_Game, KachuPOP, 225 , 400, "flat", 0)
            print("皮卡丘充電！！")
            canvas_Game.itemconfig("BG", image = KachuBG)
            canvas_Game.itemconfig("Title", image = KachuTitle)
            canvas_Game.itemconfig("mod_1", text = "")
            
        else :
            canvas_Game.itemconfig("BG", image = BG)
            canvas_Game.itemconfig("Title", image = Title)
            canvas_Game.itemconfig("mod_1", text = "")
            switch_music(self.bgm_playing, bgm,game_running)

    def Kachu_init(self, canvas_Game):
        
        update_picture(canvas_Game , "LP" , KachuQST)
        update_picture(canvas_Game , "MP" , KachuQST)
        update_picture(canvas_Game , "RP" , KachuQST)

        canvas_Game.itemconfig("Add", text=f"")
        canvas_Game.itemconfig("Score", text= f"目前分數：{self.score}")
        canvas_Game.itemconfig("Times", text= f"剩餘次數：{self.times - self.ed}")
        canvas_Game.itemconfig("mod_2", text = f"")

