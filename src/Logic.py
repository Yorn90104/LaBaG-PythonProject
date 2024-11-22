from src.Game import Game


LABAG = Game()

def button_able(win , canvas_Game , button_begin, frame_Game, frame_End, canvas_End, button_music):
      """按鈕啟用"""
      win.bind('<space>', lambda event: Begin(win , canvas_Game , button_begin, frame_Game, frame_End, canvas_End, button_music))
      button_begin.config(state='normal')

def button_unable(win , button_begin) :
      """按鈕停用"""
      win.unbind('<space>')  # 取消space鍵的綁定
      button_begin.config(state='disabled')  # 停用按鈕

def Begin(win, canvas_Game, button_begin, frame_Game, frame_End, canvas_End, button_music):
     print("\n按鈕已被按下")
     button_unable(win, button_begin)
     LABAG.super_times(canvas_Game)
     LABAG.green_times(canvas_Game)

     mod = LABAG.now_mod()
     if mod == "SuperHHH":
          LABAG.Super_init(canvas_Game)
     elif mod == "GreenWei":
          LABAG.Green_init(canvas_Game)
     elif mod == "PiKaChu":
          LABAG.Kachu_init(canvas_Game)
     else:
          LABAG.normal_init(canvas_Game)

     if LABAG.ed < LABAG.times :
          
          #產生隨機數
          LABAG.random_value()
          LABAG.super_ram()
          LABAG.green_ram()
          
          #分類p
          LABAG.p1 =LABAG.classify_p(LABAG.ram1)
          LABAG.p2 =LABAG.classify_p(LABAG.ram2)
          LABAG.p3 =LABAG.classify_p(LABAG.ram3)
          LABAG.all_p = [LABAG.p1, LABAG.p2, LABAG.p3]

          LABAG.judge_super(win, canvas_Game) #判斷阿禾

          #每隔0.5秒改圖片
          win.after(500 , lambda: LABAG.change_picture(canvas_Game , "LP" , LABAG.p1))
          win.after(1000 , lambda: LABAG.change_picture(canvas_Game , "MP" , LABAG.p2))
          win.after(1500 , lambda: LABAG.change_picture(canvas_Game , "RP" , LABAG.p3))

          #計算分數
          LABAG.calculate_score()
          LABAG.add *= LABAG.times_dict[LABAG.now_mod()] #加分倍數
          print(f"加分倍數：{LABAG.times_dict[LABAG.now_mod()]}")

          LABAG.judge_green(win, canvas_Game) #判斷綠光
     
          #結果呈現
          win.after(3000,LABAG.result)
          win.after(3000, lambda: LABAG.result_txt(canvas_Game))

          LABAG.judge_kachu(win, canvas_Game) #判斷卡秋

          if LABAG.ed + 1 >= LABAG.times :
               #遊戲結束
               win.after(3500 , LABAG.game_over)
               win.after(3500 , lambda : LABAG.to_end_frame(canvas_End, frame_Game, frame_End, button_music))

               #在特殊模式下還原
               LABAG.judge_super(win, canvas_Game, False)
               LABAG.judge_green(win, canvas_Game, False)
               LABAG.judge_kachu(win, canvas_Game, False)
               

          else:
               # 遊戲繼續
               win.after(3500 , lambda : button_able(win, canvas_Game, button_begin, frame_Game, frame_End, canvas_End, button_music))
