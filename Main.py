from src.GUI import (
                        setup_tk_win, setup_frame_and_canvas,switch_frame, init_window_mainloop,#視窗
                        input_box, get_input, reset_input_box, load_picture, add_text, image_button, txt_button, #圖像元素
                        save_icon
                        )
from src.imageb64 import image_dict

save_icon(image_dict, 'Superhhh')
win = setup_tk_win("啦八機", "temp_icon.ico", 450, 800)

from src.Logic import LABAG, Begin, button_able
from src.Element import (
                            BG, QST, Title, SuperCircle, SB, 
                            back, BeginPIC, AgainPIC
                            )
from src.Sheet import get_data

get_data()

frame_Home, canvas_Home = setup_frame_and_canvas(win, 450, 800, BG)
frame_Game, canvas_Game = setup_frame_and_canvas(win, 450, 800, BG)
frame_End, canvas_End = setup_frame_and_canvas(win, 450, 800, BG)


button_music = txt_button(
                        win,
                        lambda : LABAG.bgm_on_off(button_music),
                        "關",
                        33, 33,
                        415, 765,
                        14,
                        "black",
                        "#C0C0C0"
                        )


#region HOME畫面
def into_game():
    """進入遊戲"""
    Name = get_input(input_name)
    if Name != "" :
        canvas_Game.itemconfig("Name", text =  f"玩家名：{Name}")
        print(f"玩家名：{Name}")
    else :
        canvas_Game.itemconfig("Name", text =  "")
        print(f"玩家名：無")

    switch_frame(frame_Home, frame_Game)
    print("切換遊戲畫面")
    win.unbind('<Return>')
    win.bind('<space>', lambda event :Begin(win , canvas_Game , button_begin, frame_Game, frame_End, canvas_End, button_music))# 綁定 space 鍵
    LABAG.game_start_reset(canvas_Game, Name)
    LABAG.bgm_on_off(button_music)

input_name = input_box(
                        win,
                        canvas_Home, 
                        "",
                        225, 550,
                        18, 15
                        )

pic_SuperCircle = load_picture(canvas_Home, SuperCircle, 50, 130, "SuperCircle")
canvas_Home.tag_bind("SuperCircle", "<Button-1>", lambda event :into_game())
win.bind('<Return>', lambda event :into_game()) #綁定ENTER進入遊戲

text_fanyu = add_text(
                canvas_Home,
                "作者IG：fan._.yuuu",
                225, 100,
                30,
                "#00FFFF",
                "fanyu"
                )

text_click = add_text(
                canvas_Home,
                "點擊上方圖片(或 ENTER )\n       進入遊戲 >>>>>",
                225, 500,
                15,
                "#FFFFAA",
                "click" 
                )

text_hint = add_text(
                canvas_Home,
                "輸入你的稱呼",
                225, 575,
                12,
                "white",
                "hint"
                )

#endregion

#region GAME畫面

pic_title = load_picture(canvas_Game , Title , 0 , 25 , "Title")

load_picture(canvas_Game , QST, 0, 250 , "LP")
load_picture(canvas_Game , QST, 150, 250 , "MP")
load_picture(canvas_Game , QST, 300, 250 , "RP")


def back_home():
    """返回首頁"""
    reset_input_box(input_name, LABAG.name)
    switch_frame(frame_Game, frame_Home)
    LABAG.bgm_on_off(button_music,False)
    win.unbind('<space>')  # 取消space鍵的綁定
    win.bind('<Return>', lambda event :into_game())

    print("返回首頁")
    
button_back = image_button(
                        win,
                        back_home,
                        canvas_Game,
                        back,
                        18, 18
                        )


button_begin = image_button(
                        win ,
                        lambda :Begin(win, canvas_Game, button_begin, frame_Game, frame_End, canvas_End, button_music) ,
                        canvas_Game,
                        BeginPIC,
                        225, 575
                        )


text_name_Game = add_text(
                canvas_Game,
                "",
                5, 50,
                15,
                "white",
                "Name",
                "w"
                )
text_add = add_text(
                canvas_Game ,
                "" ,
                225 , 478 ,
                16 ,
                "yellow" ,
                "Add"
                )
text_score = add_text(
                canvas_Game ,
                "" ,
                225 , 500 ,
                16 ,
                "white" ,
                "Score"
                )
text_times = add_text(
                canvas_Game ,
                "" ,
                225 , 525 ,
                16 ,
                "white" ,
                "Times"
                )
text_history_score = add_text(
                canvas_Game ,
                "" ,
                5, 775 ,
                16 ,
                "#FFBF00",
                "history_score",
                "w" #靠左對齊
                )
#region 特殊模式顯示次數文字
text_mod1 = add_text(
                canvas_Game ,
                "" ,
                225 , 650 ,
                16 ,
                "white",
                "mod_1",
                )

text_mod2 = add_text(
                canvas_Game ,
                "" ,
                225 , 460 ,
                10 ,
                "white",
                "mod_2",
                )

text_gss = add_text(
                canvas_Game ,
                f"咖波累積數：{LABAG.gss_times}" ,
                445 , 50 ,
                14 ,
                "#00FF00",
                "gss",
                "e"
                )

#endregion


#region END畫面
def game_again():
    """再一次遊戲"""
    switch_frame(frame_End, frame_Game)
    print("切換至遊戲畫面")
    LABAG.game_start_reset(canvas_Game, LABAG.name)
    LABAG.bgm_on_off(button_music)
    button_able(win, canvas_Game, button_begin, frame_Game, frame_End, canvas_End, button_music)

text_name_End = add_text(
                canvas_End,
                "",
                225, 175,
                22,
                "skyblue",
                "Name",
                )
text_over = add_text(
                canvas_End ,
                "遊戲結束！" ,
                225 , 260 ,
                42 ,
                "white" ,
                "over"
                )
text_final_score = add_text(
                        canvas_End ,
                        "" ,
                        225 , 325 ,
                        32 ,
                        "#FF0000" ,
                        "final_score"
                        )
text_HS = add_text(
                canvas_End ,
                f"歷史最高分數：{LABAG.history_score}" ,
                225, 450 ,
                16 ,
                "#FFBF00" ,
                "HS"
                )

button_again = image_button(
                        win,
                        game_again,
                        canvas_End,
                        AgainPIC,
                        225, 400
                        )

pic_SB = load_picture(canvas_End , SB, 0, 500, "SB")


init_window_mainloop(win, frame_Home)