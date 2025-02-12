from GUI import Window
win = Window("啦八機", 450, 800) #先初始化 Tkinter 才能創建 ImageTk
from src.Game import P, PlayLaBaG, JsonLaBaG
from src.element import (
    Gss, Hhh, Hentai, Handsun, Kachu, Rrr,
    BG, SuperBG, GreenBG, KachuBG,
    QST, SuperQST, GreenQST, KachuQST, 
    Title, SuperTitle, GreenTitle, KachuTitle, 
    SuperPOP, GreenPOP, KachuPOP,
    image_dict, music,
    SuperCircle, 
    back, BeginPIC, AgainPIC, SB,
    super_hhh, 
    green_wei, GreenLeft, GreenMid, GreenRight,
    pikachu
)
from src.Sheet import Sheet

Sheet.GetData() #獲取啦八機試算表的資料

Games = {
    "Game": PlayLaBaG(),
    "Json_Game" : JsonLaBaG() #.json檔案模擬用
}  
Game = Games["Game"] #預設
P.Dict["A"].picture = Gss
P.Dict["B"].picture = Hhh
P.Dict["C"].picture = Hentai
P.Dict["D"].picture = Handsun
P.Dict["E"].picture = Kachu
P.Dict["F"].picture = Rrr

win.save_icon_use(image_dict, "Superhhh")
#創建 Screen(frame & canvas)
win.setup_frame_and_canvas("Home", BG) #首頁
win.setup_frame_and_canvas("Game", BG) #遊戲畫面
win.setup_frame_and_canvas("End", BG) #結算畫面

win.temp_files = music.temp_files # 連結臨時檔案 list


#region Home Screen

win.load_picture("Home", SuperCircle, 50, 130, "SuperCircle")

def into_game():
    """進入Game畫面"""
    global Game
    Game = Games["Game"]
    Game.Name = win.get_input("Name")
    if Game.Name:
        win.update_by_tag("Game", "PlayerName", f"玩家名：{Game.Name}")
        print(f"玩家名：{Game.Name}")
    else :
        win.update_by_tag("Game", "PlayerName", f"")
        print(f"玩家名：無")

    Game.history_score = Sheet.GetScore(Game.Name)
    win.unbind('<Return>') # 解除綁定ENTER
    BeginAble()
    Game.Reset()
    init_Game_screen_item()
    bgm_on_off()
    win.switch_frame("Home", "Game") #切換畫面

win.Canva("Home").tag_bind("SuperCircle", "<Button-1>", lambda event :into_game()) #綁定 SuperCircle 圖片被點擊->進入遊戲
win.bind('<Return>', lambda event :into_game()) #綁定ENTER進入遊戲

win.input_box(
    "Home", 
    "Name", #Name 輸入盒
    "",
    225, 550,
    18, 15
)

win.add_text(
    "Home",
    "作者IG：fan._.yuuu",
    225, 100,
    30,
    "#00FFFF",
    "fanyu"
)

win.add_text(
    "Home",
    "點擊上方圖片(或 ENTER )\n       進入遊戲 >>>>>",
    225, 500,
    15,
    "#FFFFAA",
    "click" 
)

win.add_text(
    "Home",
    "輸入你的稱呼",
    225, 575,
    12,
    "white",
    "hint"
)

def into_json():
    """進入Json_Game畫面"""
    import os
    #判斷路徑是否為空、是否存在、是否為.json檔
    json_path = win.open_file()
    if json_path is not None and os.path.exists(json_path) and os.path.splitext(json_path)[1] == ".json":
        global Game
        Game = Games["Json_Game"]
        win.Canva("Game").itemconfig("PlayerName", text =  "正在使用 .json檔案模擬")
        print(f"使用 .json檔案模擬中")
        Game.setup_path(f"{json_path}")

        BeginAble()
        Game.Reset()
        init_Game_screen_item()
        bgm_on_off()
        win.switch_frame("Home", "Game") #切換畫面
    else:
        win.message_box(
            f"無效的路徑:\n{json_path}",
            )
        print(f"無效的路徑:\n{json_path}")

win.txt_button(
    "toJson",
    into_json,
    "Home",
    "使用 .json 檔案模擬遊戲",
    10, 2,
    110, 770,
    12,
    "black", "yellow"
)

def rank_subwindow():
    """排行榜子視窗"""
    win.Button("toRank").config(state='disabled') # toRank Button 停用
    win.Button("toRank").config(text="資料載入中")
    Sheet.GetData() #獲取資料
    win.setup_subwindow("Rank", 450, 800, BG)

    win.SubWindow("Rank").add_text(
        "排行榜",
        225, 50,
        30,
        "yellow",
        "Title"
        )
    
    
    for index, data in enumerate(list(Sheet.RankedData().items())[:10]): # 顯示前 10 名
        win.SubWindow("Rank").add_text(
            f"{index + 1 :<2}. {data[0]:<10s} : {data[1] :>8,}",
            50, 125 + index * 50,
            16,
            "white",
            f"rank_{index}",
            "w"
            )
    
    def off_rank():
        """關閉排行榜子視窗"""
        win.Button("toRank").config(state='normal')
        win.Button("toRank").config(text="查看排行榜")
        win.SubWindow("Rank").destroy()
    win.SubWindow("Rank").txt_button(
        "off_window",
        off_rank,
        "關閉視窗",
        100, 50,
        225, 700,
        16
        )
    win.SubWindow("Rank").protocol("WM_DELETE_WINDOW", off_rank) #綁定關閉視窗
    

win.txt_button(
    "toRank",
    rank_subwindow,
    "Home",
    "查看排行榜",
    10, 2,
    225, 50,
    12,
    "black", "white"
)
#endregion


#region Game Screen
def init_Game_screen_item():
    """初始化 Game 畫面物件"""
    win.update_by_tag("Game", "BG", BG)
    win.update_by_tag("Game", "LP", QST)
    win.update_by_tag("Game", "MP", QST)
    win.update_by_tag("Game", "RP", QST)
    win.update_by_tag("Game", "Title", Title)
    win.update_by_tag("Game", "MarginScore", f"")
    win.update_by_tag("Game", "Score", f"目前分數：{Game.score}")
    win.update_by_tag("Game", "Times", f"剩餘次數：{Game.times - Game.played}")
    win.update_by_tag("Game", "history_score", f"歷史最高分數：{Game.history_score}")
    win.update_by_tag("Game", "mod_1", f"")
    win.update_by_tag("Game", "mod_2", f"")
    win.update_by_tag("Game", "gss", f"咖波累積數：{Game.GssNum}")

def Game_to_Home():
    """返回首頁"""
    win.reset_input_box("Name", Game.Name)
    win.unbind('<space>')  # 取消space鍵的綁定
    win.bind('<Return>', lambda event :into_game())
    bgm_on_off(game_running=False) #關閉音樂
    win.switch_frame("Game", "Home")
    print("返回首頁")

win.image_button(
    win,
    Game_to_Home,
    "Game",
    back,
    18, 18
)

win.load_picture("Game" , Title , 0 , 25 , "Title")
win.load_picture("Game" , QST, 0, 250 , "LP")
win.load_picture("Game" , QST, 150, 250 , "MP")
win.load_picture("Game" , QST, 300, 250 , "RP")

def BeginAble():
    """可 Begin"""
    win.bind('<space>', lambda event: Begin()) # 綁定Space鍵
    win.Button("Begin").config(state='normal') # Begin Button 啟用

def BeginUnable() :
      """不可 Begin"""
      win.unbind('<space>')  # 取消space鍵的綁定
      win.Button("Begin").config(state='disabled')  # Begin Button 停用

def Begin():
    """開始"""  
    def resetQST():
        """根據模式重置QST圖片"""
        match Game.NowMode():
            case "SuperHHH":
                qstpic = SuperQST
            case "GreenWei":
                qstpic = GreenQST
            case "PiKaChu":
                qstpic = KachuQST
            case _:
                qstpic = QST

        win.update_by_tag("Game", "LP", qstpic)
        win.update_by_tag("Game", "MP", qstpic)
        win.update_by_tag("Game", "RP", qstpic)

        win.update_by_tag("Game", "MarginScore", "") #邊際分數文字清除
        win.update_by_tag("Game", "mod_2", "")

    def change_pic_per500ms():
        """每隔0.5秒改圖片"""
        win.after(500, lambda: win.update_by_tag("Game", "LP", Game.Ps[0].picture))
        win.after(1000, lambda: win.update_by_tag("Game", "MP", Game.Ps[1].picture))
        win.after(1500, lambda: win.update_by_tag("Game", "RP", Game.Ps[2].picture))
        # Ding 音效
        win.after(500, lambda: music.play_sound("Ding"))
        win.after(1000, lambda: music.play_sound("Ding"))
        win.after(1500, lambda: music.play_sound("Ding"))

    def picture_and_sound():
        match Game.NowMode():
            case "Normal":
                return
            
            case "SuperHHH":
                if Game.Ps[0].code == "B":
                    win.update_by_tag("Game", "LP" , super_hhh)
                if Game.Ps[1].code == "B":
                    win.update_by_tag("Game", "MP" , super_hhh)
                if Game.Ps[2].code == "B":
                    win.update_by_tag("Game", "RP" , super_hhh)
                music.play_sound("SuperUP")
            
            case "GreenWei":
                if all(p.code == "A" for p in Game.Ps):
                    win.update_by_tag("Game", "LP" , GreenLeft)
                    win.update_by_tag("Game", "MP" , GreenMid)
                    win.update_by_tag("Game", "RP" , GreenRight)
                elif any(p.code == "A" for p in Game.Ps):
                    if Game.Ps[0].code == "A":
                        win.update_by_tag("Game", "LP" , green_wei)
                    if Game.Ps[1].code == "A":
                        win.update_by_tag("Game", "MP" , green_wei)
                    if Game.Ps[2].code == "A":
                        win.update_by_tag("Game", "RP" , green_wei)
                else:
                    win.update_by_tag("Game", "LP" , green_wei)
                    win.update_by_tag("Game", "MP" , green_wei)
                    win.update_by_tag("Game", "RP" , green_wei)
                music.play_sound("GreenUP")
            case "PiKaChu":
                music.switch_music("KachuMusic")
                if Game.Ps[0].code == "E":
                    win.update_by_tag("Game", "LP" , pikachu)
                if Game.Ps[1].code == "E":
                    win.update_by_tag("Game", "MP" , pikachu)
                if Game.Ps[2].code == "E":
                    win.update_by_tag("Game", "RP" , pikachu)

    def screen_pop_music():
        """畫面、彈出圖片、音樂"""
        match Game.NowMode():
            case "Normal":
                win.update_by_tag("Game", "BG", BG)
                win.update_by_tag("Game", "Title", Title)
                win.update_by_tag("Game", "mod_1", f"")
                music.switch_music("bgm")

            case "SuperHHH":
                win.image_button("pop", lambda: win.delete_canvas_tag("Game", "pop"), "Game", SuperPOP, 225 , 400, "flat", 0)
                win.update_by_tag("Game", "BG", SuperBG)
                win.update_by_tag("Game", "Title", SuperTitle)
                win.Canva("Game").itemconfig("mod_1", text = f"超級阿禾剩餘次數:{Game.SuperTimes}次", fill = "#FF00FF")
                music.switch_music("SuperMusic")
                if Game.double_score > 0:
                    win.Canva("Game").itemconfig("mod_2", text = f"(超級阿禾加倍分:{Game.double_score})", fill = "yellow")

            case "GreenWei":
                win.image_button("pop", lambda: win.delete_canvas_tag("Game", "pop"), "Game", GreenPOP, 225 , 400, "flat", 0)
                win.update_by_tag("Game", "BG", GreenBG)
                win.update_by_tag("Game", "Title", GreenTitle)
                win.Canva("Game").itemconfig("mod_1", text =  f"綠光阿瑋剩餘次數:{Game.GreenTimes}次", fill = "#00FF00")
                music.switch_music("GreenMusic")

            case "PiKaChu":
                win.image_button("pop", lambda: win.delete_canvas_tag("Game", "pop"), "Game", KachuPOP, 225 , 400, "flat", 0)
                win.update_by_tag("Game", "BG", KachuBG)
                win.update_by_tag("Game", "Title", KachuTitle)
                win.Canva("Game").itemconfig("mod_1", text = f"已觸發 {Game.kachu_times} 次皮卡丘充電", fill = "#FFFF00")
           
    def result_txt():
        """顯示結果文字"""
        win.update_by_tag("Game", "MarginScore", f"+{Game.margin_score}")
        win.update_by_tag("Game", "Score", f"目前分數：{Game.score}")
        win.update_by_tag("Game", "Times", f"剩餘次數：{Game.times - Game.played}")
        win.update_by_tag("Game", "gss", f"咖波累積數：{Game.GssNum}")
        match Game.NowMode():
            case "SuperHHH":
                win.Canva("Game").itemconfig("mod_1", text = f"超級阿禾剩餘次數:{Game.SuperTimes}次", fill = "#FF00FF")
            case "GreenWei":
                win.Canva("Game").itemconfig("mod_1", text =  f"綠光阿瑋剩餘次數:{Game.GreenTimes}次", fill = "#00FF00")


    #Main
    win.delete_canvas_tag("Game", "pop")
    BeginUnable()
    resetQST()
    Game.Logic()
    change_pic_per500ms()
    win.after(3000, result_txt)
    if not Game.GameRunning():
        Game.GameOver()
        Sheet.CommitScore(Game.Name, Game.score)
        win.after(3500, Game_over_to_End)
        return
    if Game.ModtoScreen:
        win.after(2800, picture_and_sound)
        win.after(3500, screen_pop_music)
    win.after(3500, BeginAble)
    return

#開始按紐
win.image_button(
    "Begin",
    Begin,
    "Game",
    BeginPIC,
    225, 575
)

win.add_text(
    "Game",
    "",
    5, 50,
    15,
    "white",
    "PlayerName", #Game.Name
    "w"
)

win.add_text(
    "Game" ,
    "" ,
    225 , 478 ,
    16 ,
    "yellow" ,
    "MarginScore" # Game.margin_score
)

win.add_text(
    "Game" ,
    "" ,
    225 , 500 ,
    16 ,
    "white" ,
    "Score" #Game.score
)

win.add_text(
    "Game",
    "",
    225, 525,
    16,
    "white",
    "Times" #Game.times - Game.played
)

win.add_text(
    "Game" ,
    "" ,
    5, 775 ,
    16 ,
    "#FFBF00",
    "history_score", #Game.history_score
    "w" #靠左對齊
)


def bgm_on_off(game_running: bool= True) :
    """音樂開 & 關"""
    match Game.NowMode():
        case "SuperHHH":
            file_name = "SuperMusic"
        case "GreenWei":
            file_name = "GreenMusic"
        case "PiKaChu":
            file_name = "KachuMusic"
        case _:
            file_name = "bgm"
    
    #關
    if music.bgm_playing or not game_running:
        music.stop_music()
        win.Button("music").config(text="關", bg="#C0C0C0") 
        print("BGM已停止")
    #開
    else :
        music.play_music(file_name) 
        win.Button("music").config(text="開", bg="#00FF00")
        print("BGM已開啟")

win.txt_button(
    "music",
    bgm_on_off,
    "Game",
    "關",
    33, 33,
    415, 765,
    14,
    "black",
    "#C0C0C0"
)

#特殊模式顯示次數文字
win.add_text(
    "Game",
    "" ,
    225 , 650 ,
    16 ,
    "white",
    "mod_1",
) 

win.add_text(
    "Game",
    "" ,
    225 , 460 ,
    10 ,
    "white",
    "mod_2",
)

win.add_text(
    "Game",
    f"咖波累積數：{Game.GssNum}" ,
    445 , 50 ,
    14 ,
    "#00FF00",
    "gss",
    "e"
)


#endregion

#region End Screen
def Game_over_to_End():
    bgm_on_off(Game.GameRunning())
    music.play_sound("Ding")
    print("切換至結束畫面")
    win.update_by_tag("End", "PlayerName", f"{Game.Name}")
    win.update_by_tag("End","over", "遊戲結束！") 
    win.update_by_tag("End","final_score", f"最終分數：{Game.score}")  # 最終分數顯示
    win.update_by_tag("End","history_score", f"歷史最高分數：{Game.history_score}")
    win.switch_frame("Game", "End")
    

def game_again():
    """再玩一次遊戲"""
    BeginAble()
    Game.Reset()
    init_Game_screen_item()
    bgm_on_off()
    win.switch_frame("End", "Game")

win.add_text(
    "End",
    "",
    225, 175,
    22,
    "skyblue",
    "PlayerName", #Game.Name
)

win.add_text(
    "End" ,
    "遊戲結束！" ,
    225 , 260 ,
    42 ,
    "white" ,
    "over"
)

win.add_text(
    "End" ,
    "" ,
    225 , 325 ,
    32 ,
    "#FF0000" ,
    "final_score" #Game.score
)

win.add_text(
    "End" ,
    f"歷史最高分數：{Game.history_score}" ,
    225, 450 ,
    16 ,
    "#FFBF00" ,
    "history_score" #Game.history_score
)

win.image_button(
    "Again",
    game_again,
    "End",
    AgainPIC,
    225, 400
)

def save_json():
    """保存.json檔案"""
    if isinstance(Game, JsonLaBaG):
        print(f"此為json檔模擬模式 無法再次保存")
        win.message_text(
                2000,
                "End",
                f"此為json檔模擬模式 無法再次保存",
                225, 730
            )     
        return

    import os
    import json
    from datetime import datetime
    # 確保目錄存在
    output_dir = "C:\\JsonLaBaG\\"
    os.makedirs(output_dir, exist_ok=True)
    # 使用時間戳作為部分文件名
    timestamp = datetime.now().strftime("%Y%m%d")
    filename = f"{output_dir}{Game.score}_{timestamp}.json"
    try: 
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(Game.AllData, file, indent=4)
            print(f"保存成功: {filename}")

            win.message_text(
                2000,
                "End",
                f"已成功保存至: {filename}",
                225, 730
            )
    except Exception as e:
        print(f"無法保存: {e}")
        win.message_box(
                f"無法保存: {e}",
            )

win.txt_button(
    "save_json",
    save_json,
    "End",
    "保存本次紀錄(.json)",
    10, 2,
    225, 700,
    12,
    "black", "#00FF00"
    
)

win.load_picture("End" , SB, 0, 500, "SB")
#endregion


win.first_window("Home")
win.mainloop()