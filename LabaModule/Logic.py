from random import randint
from LabaModule.Var import (
                        ram1, ram2, ram3,
                        p1, p2, p3, all_p,
                        normal_acc,super_acc,
                        score, history_score, add,
                        ed, times,
                        same1, same2, same3
                        )
from LabaModule.UI import  init , change_picture, result_txt 
from LabaModule.Sound import Ding , bgm_on_off

from LabaModule.SuperHhh import super_ram, judge_super, super_times, switch_super_rate

# 主要邏輯流程：
# 按鈕或鍵盤事件觸發 Begin 函數。
# 重置畫面，並初始化變量。
# 生成三個隨機數，每個隨機數對應不同的圖片。
# 按時間間隔改變畫面中的三張圖片，每隔 0.5 秒更新一張圖片。
# 計算得分，根據三張圖片的組合（是否相同）來計算加分。
# 顯示結果，更新畫面上的分數、加分和剩餘次數。


def result(canvas_Game):
      """計算和顯示結果"""
      global score, add, ed, p1, p2, p3 
      ed += 1
      score += add
      print(f"第{ed}次")
      print(f' | {p1} | {p2} | {p3} |')
      print(f"+{add}")
      print(f"目前分數：{score}")
      result_txt(canvas_Game , score , add , ed , times)
      add = 0

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

def ADD(x, y, lst):
    """增加分數 (歸屬, 增加分數, 分數清單)"""
    if x == 'A':
        y += lst[0]
    elif x == 'B':
        y += lst[1]
    elif x == 'C':
        y += lst[2]
    elif x == 'D':
        y += lst[3]
    elif x == 'E':
        y += lst[4]
    elif x == 'F':
        y += lst[5]
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

def button_unable(win , button) :
      win.unbind('<space>')  # 取消space鍵的綁定
      button.config(state='disabled')  # 停用按鈕

def button_able(win , canvas_Game , button_begin, frame_Game, frame_End, canvas_End, button_music):
      win.bind('<space>', lambda event: Begin(win , canvas_Game , button_begin, frame_Game, frame_End, canvas_End, button_music))
      button_begin.config(state='normal')

def history_score_txt(canvas_End):
      global score, history_score
      if score > history_score :
            history_score = score
            canvas_End.itemconfig("HS", text=f"歷史最高分數：{history_score}" ) 

def game_over(frame_Game, frame_End, canvas_End, button_music):
      global score, history_score, times, ed 
      print("遊戲已結束")
      print(f"最終分數為：{score}")
      bgm_on_off(button_music, game_running = False)
      """遊戲結束，切換到結果頁面"""
      frame_Game.pack_forget()  # 隱藏遊戲畫面
      print("切換End畫面")
      frame_End.pack(fill='both', expand=True)  # 顯示遊戲結束畫面
      canvas_End.itemconfig("over", text="遊戲結束！") 
      canvas_End.itemconfig("final_score", text=f"最終分數：{score}")  # 最終分數顯示
      history_score_txt(canvas_End) #歷史分數更新
      Ding()

def game_again(win , canvas_Game , button_begin, frame_Game, frame_End, canvas_End, button_music) :
      global ram1 , ram2 , ram3 , p1 , p2 , p3 , score , add , ed  , times, history_score
      ram1, ram2, ram3 = 0 , 0 , 0
      p1, p2, p3 = '', '', ''
      score, add, ed = 0 , 0 , 0

      init(canvas_Game, score, times , ed)
      bgm_on_off(button_music)
      canvas_Game.itemconfig("history_score", text=f"歷史最高分數：{history_score}" ) 
      button_able(win , canvas_Game , button_begin, frame_Game, frame_End, canvas_End, button_music)
      frame_End.pack_forget()
      print("切換Game畫面")
      frame_Game.pack(fill='both', expand=True)


def Begin(win , canvas_Game , button_begin, frame_Game, frame_End, canvas_End, button_music) :
      global ram1, ram2, ram3, p1, p2, p3, all_p,  score, add, ed, normal_acc, super_acc

      print(u"\n按鈕被點擊了！")
      super_times(win,canvas_Game)
      button_unable(win , button_begin)

      init(canvas_Game, score, times , ed)
      

      if ed  < times :

            #隨機數
            ram1 , ram2 , ram3 = randint(1,100) , randint(1,100) , randint(1,100)
            print(f"圖片隨機數為：{ram1} | {ram2} | {ram3}")
            super_ram()
            

            #機率找歸屬
            use_rate = switch_super_rate(normal_acc,super_acc)
            print(use_rate)
            p1 = change_rate(use_rate, ram1)
            p2 = change_rate(use_rate, ram2)
            p3 = change_rate(use_rate, ram3)
            
            all_p = [p1, p2, p3]
            judge_super(win, canvas_Game, all_p, add, score, button_music)

            #每隔0.5秒改圖片
            win.after(500 , lambda : change_picture(canvas_Game , "LP" , p1))
            win.after(1000 , lambda : change_picture(canvas_Game , "MP" , p2))
            win.after(1500 , lambda : change_picture(canvas_Game , "RP" , p3))

            #增加分數
            add = calculate_score(p1 , p2 , p3 , add)
            
            win.after(3000 , lambda : result(canvas_Game))

            if ed + 1 >= times:
                # 判斷遊戲結束
                # 停用按鈕和鍵盤事件
                win.after(3500, lambda : button_unable(win, button_begin))

                # 切換到結束畫面
                win.after(3500, lambda : game_over(frame_Game , frame_End , canvas_End, button_music))
                
                #若在超級阿禾模式則還原
                judge_super(win, canvas_Game, all_p, add, score, button_music, False)

                
            else:
                judge_super(win, canvas_Game, all_p, add, score, button_music)
                # 遊戲繼續
                win.after(3500 , lambda : button_able(win, canvas_Game, button_begin, frame_Game, frame_End, canvas_End, button_music))