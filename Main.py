from GUI import Window
win = Window("啦八機", 450, 800) #先初始化 Tkinter 才能創建 ImageTk
from src.Game import P, LaBaG, JsonLaBaG
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
    "Game": LaBaG(),
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
win.setup_frame_and_canvas("Json_Game", BG) # .json檔案模擬遊戲畫面

win.temp_files = music.temp_files # 連結臨時檔案 list


#region Home Screen

win.load_picture("Home", SuperCircle, 50, 130, "SuperCircle")

def into_game():
    """進入Game畫面"""
    global Game
    Game = Games["Game"]
    Game.name = win.get_input("Name")
    if Game.name:
        win.update_text("Game", "PlayerName", f"玩家名：{Game.name}")
        print(f"玩家名：{Game.name}")
    else :
        win.update_text("Game", "PlayerName", f"")
        print(f"玩家名：無")

    Game.history_score = Sheet.GetScore(Game.name)
    win.unbind('<Return>') # 解除綁定ENTER
    BeginAble()
    Game.reset()
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

def into_json(json_path: str= None):
    """進入Json_Game畫面"""
    import os
    #判斷路徑是否為空、是否存在、是否為.json檔
    if json_path is not None and os.path.exists(json_path) and os.path.splitext(json_path)[1] == ".json":
        global Game
        Game = Games["Json_Game"]
        win.Canva("Game").itemconfig("PlayerName", text =  "正在使用 .json檔案模擬")
        print(f"使用 .json檔案模擬中")
        Game.setup_path(f"{json_path}")

        win.unbind('<Return>') # 解除綁定ENTER
        win.SubWindow("JsonPath").unbind('<Return>')
        BeginAble()
        Game.reset()
        init_Game_screen_item()
        bgm_on_off()
        win.switch_frame("Home", "Game") #切換畫面
        win.SubWindow("JsonPath").destroy()
    else:
        win.SubWindow("JsonPath").message_text(
            1000,
            f"無效 or 不存在的路徑: {json_path}",
            150, 130,
            10,
            "red"
            )
        print(f"無效 or 不存在的路徑: {json_path}")


def jsonpath_subwindow():
    """json路徑子視窗"""
    win.setup_subwindow("JsonPath", 300, 200, BG)
    win.SubWindow("JsonPath").add_text(
        "請輸入 .json檔案之路徑\n      (絕對or相對都行)",
        150, 50,
        14,
        "white",
        "path"
    )
    win.SubWindow("JsonPath").input_box(
        "path",
        "",
        150, 100,
        12,
        18
    )
    win.SubWindow("JsonPath").txt_button(
        "commit_path",
        lambda: into_json(win.SubWindow("JsonPath").get_input("path")),
        "提交路徑",
        10, 2,
        150, 160,
        12
    )
    win.SubWindow("JsonPath").bind('<Return>', lambda event: into_json(win.SubWindow("JsonPath").get_input("path")))

win.txt_button(
    "toJson",
    jsonpath_subwindow,
    "Home",
    "使用 .json 檔案模擬遊戲",
    10, 2,
    110, 770,
    12,
    "black", "yellow"
)

def rank_subwindow():
    """排行榜子視窗"""
    win.setup_subwindow("Rank", 450, 800, BG)

    win.SubWindow("Rank").add_text(
        "排行榜",
        225, 50,
        30,
        "yellow",
        "Title"
        )
    
    
    for index, data in enumerate(Sheet.RankedData()[:10]): # 顯示前 10 名
        win.SubWindow("Rank").add_text(
            f"{index + 1 :<2}. {data[0]:<10s} : {data[1] :>8,}",
            50, 125 + index * 50,
            16,
            "white",
            f"rank_{index}",
            "w"
            )
    
    win.SubWindow("Rank").txt_button(
        "off_window",
        win.SubWindow("Rank").destroy,
        "關閉視窗",
        100, 50,
        225, 700,
        16
        )

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
    win.update_picture("Game", "BG", BG)
    win.update_picture("Game", "LP", QST)
    win.update_picture("Game", "MP", QST)
    win.update_picture("Game", "RP", QST)
    win.update_picture("Game", "Title", Title)
    win.update_text("Game", "MarginScore", f"")
    win.update_text("Game", "Score", f"目前分數：{Game.score}")
    win.update_text("Game", "Times", f"剩餘次數：{Game.times - Game.played}")
    win.update_text("Game", "history_score", f"歷史最高分數：{Game.history_score}")
    win.update_text("Game", "mod_1", f"")
    win.update_text("Game", "mod_2", f"")
    win.update_text("Game", "gss", f"咖波累積數：{Game.gss_times}")

def Game_to_Home():
    """返回首頁"""
    win.reset_input_box("Name", Game.name)
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
        match Game.now_mod():
            case "SuperHHH":
                qstpic = SuperQST
            case "GreenWei":
                qstpic = GreenQST
            case "PiKaChu":
                qstpic = KachuQST
            case _:
                qstpic = QST

        win.update_picture("Game", "LP", qstpic)
        win.update_picture("Game", "MP", qstpic)
        win.update_picture("Game", "RP", qstpic)

        win.update_text("Game", "MarginScore", "") #邊際分數文字清除
        win.update_text("Game", "mod_2", "")

    def change_pic_per500ms():
        """每隔0.5秒改圖片"""
        win.after(500, lambda: win.update_picture("Game", "LP", Game.Ps[0].picture))
        win.after(1000, lambda: win.update_picture("Game", "MP", Game.Ps[1].picture))
        win.after(1500, lambda: win.update_picture("Game", "RP", Game.Ps[2].picture))
        # Ding 音效
        win.after(500, lambda: music.play_sound("Ding"))
        win.after(1000, lambda: music.play_sound("Ding"))
        win.after(1500, lambda: music.play_sound("Ding"))

    def picture_and_sound():
        match Game.now_mod():
            case "Normal":
                return
            
            case "SuperHHH":
                if Game.Ps[0].code == "B":
                    win.update_picture("Game", "LP" , super_hhh)
                if Game.Ps[1].code == "B":
                    win.update_picture("Game", "MP" , super_hhh)
                if Game.Ps[2].code == "B":
                    win.update_picture("Game", "RP" , super_hhh)
                music.play_sound("SuperUP")
            
            case "GreenWei":
                if all(p.code == "A" for p in Game.Ps):
                    win.update_picture("Game", "LP" , GreenLeft)
                    win.update_picture("Game", "MP" , GreenMid)
                    win.update_picture("Game", "RP" , GreenRight)
                elif any(p.code == "A" for p in Game.Ps):
                    if Game.Ps[0].code == "A":
                        win.update_picture("Game", "LP" , green_wei)
                    if Game.Ps[1].code == "A":
                        win.update_picture("Game", "MP" , green_wei)
                    if Game.Ps[2].code == "A":
                        win.update_picture("Game", "RP" , green_wei)
                else:
                    win.update_picture("Game", "LP" , green_wei)
                    win.update_picture("Game", "MP" , green_wei)
                    win.update_picture("Game", "RP" , green_wei)
                music.play_sound("GreenUP")
            case "PiKaChu":
                music.switch_music("KachuMusic")
                if Game.Ps[0].code == "E":
                    win.update_picture("Game", "LP" , pikachu)
                if Game.Ps[1].code == "E":
                    win.update_picture("Game", "MP" , pikachu)
                if Game.Ps[2].code == "E":
                    win.update_picture("Game", "RP" , pikachu)

    def screen_pop_music():
        """畫面、彈出圖片、音樂"""
        match Game.now_mod():
            case "Normal":
                win.update_picture("Game", "BG", BG)
                win.update_picture("Game", "Title", Title)
                win.update_text("Game", "mod_1", f"")
                music.switch_music("bgm")

            case "SuperHHH":
                win.image_button("pop", lambda: win.delete_button("pop"), "Game", SuperPOP, 225 , 400, "flat", 0)
                win.update_picture("Game", "BG", SuperBG)
                win.update_picture("Game", "Title", SuperTitle)
                win.Canva("Game").itemconfig("mod_1", text = f"超級阿禾剩餘次數:{Game.SuperTimes}次", fill = "#FF00FF")
                music.switch_music("SuperMusic")
                if Game.double_score > 0:
                    win.Canva("Game").itemconfig("mod_2", text = f"(超級阿禾加倍分:{Game.double_score})", fill = "yellow")

            case "GreenWei":
                win.image_button("pop", lambda: win.delete_button("pop"), "Game", GreenPOP, 225 , 400, "flat", 0)
                win.update_picture("Game", "BG", GreenBG)
                win.update_picture("Game", "Title", GreenTitle)
                win.Canva("Game").itemconfig("mod_1", text =  f"綠光阿瑋剩餘次數:{Game.GreenTimes}次", fill = "#00FF00")
                music.switch_music("GreenMusic")

            case "PiKaChu":
                win.image_button("pop", lambda: win.delete_button("pop"), "Game", KachuPOP, 225 , 400, "flat", 0)
                win.update_picture("Game", "BG", KachuBG)
                win.update_picture("Game", "Title", KachuTitle)
                win.Canva("Game").itemconfig("mod_1", text = f"已觸發 {Game.kachu_times} 次皮卡丘充電", fill = "#FFFF00")
           
    def result_txt():
        """顯示結果文字"""
        win.update_text("Game", "MarginScore", f"+{Game.margin_score}")
        win.update_text("Game", "Score", f"目前分數：{Game.score}")
        win.update_text("Game", "Times", f"剩餘次數：{Game.times - Game.played}")
        win.update_text("Game", "gss", f"咖波累積數：{Game.gss_times}")
        match Game.now_mod():
            case "SuperHHH":
                win.Canva("Game").itemconfig("mod_1", text = f"超級阿禾剩餘次數:{Game.SuperTimes}次", fill = "#FF00FF")
            case "GreenWei":
                win.Canva("Game").itemconfig("mod_1", text =  f"綠光阿瑋剩餘次數:{Game.GreenTimes}次", fill = "#00FF00")


    #Main
    if "pop" in win._button_dict:
        win.delete_button("pop")
    BeginUnable()
    resetQST()
    Game.Logic()
    change_pic_per500ms()
    win.after(3000, result_txt)
    if not Game.GameRunning():
        Game.GameOver()
        Sheet.CommitScore(Game.name, Game.score)
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
    "PlayerName", #Game.name
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
    match Game.now_mod():
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
    f"咖波累積數：{Game.gss_times}" ,
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
    win.update_text("End", "PlayerName", f"{Game.name}")
    win.update_text("End","over", "遊戲結束！") 
    win.update_text("End","final_score", f"最終分數：{Game.score}")  # 最終分數顯示
    win.update_text("End","history_score", f"歷史最高分數：{Game.history_score}")
    win.switch_frame("Game", "End")
    

def game_again():
    """再玩一次遊戲"""
    BeginAble()
    Game.reset()
    init_Game_screen_item()
    bgm_on_off()
    win.switch_frame("End", "Game")

win.add_text(
    "End",
    "",
    225, 175,
    22,
    "skyblue",
    "PlayerName", #Game.name
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

win.load_picture("End" , SB, 0, 500, "SB")
#endregion


win.first_window("Home")
win.mainloop()