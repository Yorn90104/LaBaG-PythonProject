import tkinter as tk
from LabaModule.Var import BG , QST ,L_PIC , M_PIC , R_PIC , BeginPIC , picture , text_ADD
from LabaModule.Sound import Ding

def setup_frame(win):
    """設置畫面"""
    Frame = tk.Frame(win, width=450, height=800, bg='lightblue')
    Canvas = tk.Canvas(Frame, width=450, height=800)
    Canvas.pack(fill="both", expand=True)
    Canvas.create_image(0, 0, image = BG, anchor="nw")
    return Frame, Canvas

def Load_PIC(CANVA, pc, x, y , tg):
    """加載新的圖片並放在CANVA上 (畫面 , 照片, 水平座標, 垂直座標, 標記)"""
    pic = CANVA.create_image(x, y, image = pc, anchor = "nw" , tag = tg)
    return pic

def Update_PIC(CANVA , tg ,  pc) :
    """更新CANVA上的圖片 (畫面, 標記, 圖)"""
    CANVA.itemconfig(tg , image = pc)
    # CANVA.delete(n)  # 刪除舊圖片
    # n = Load_PIC(CANVA , pc, x, y)  # 加載新圖片

def init(CANVA):
    Update_PIC(CANVA , "LP" , QST)
    Update_PIC(CANVA , "MP" , QST)
    Update_PIC(CANVA , "RP" , QST)

    CANVA.itemconfig("Add", text=f"")

def PIC(p):
    """根據歸屬選擇圖 (歸屬)"""
    if p == "A":
        return picture[0]
    elif p == "B":
        return picture[1]
    elif p == "C":
        return picture[2]
    elif p == "D":
        return picture[3]
    elif p == "E":
        return picture[4]
    elif p == "F":
        return picture[5]

def Local(CANVA , tg , p):
    """哪個變圖 (畫面, 標籤, 歸屬)"""
    new_pic = PIC(p)
    Update_PIC(CANVA, tg , new_pic)
    Ding()

def Button(win , CMD , CANVA,  x , y):
    """添加按鈕(視窗,執行動作,畫面,水平位置,垂直位置)"""
    but = tk.Button(win , image = BeginPIC , command = CMD)
    button = CANVA.create_window(x , y , window = but)
    return button

def Text(CANVA , x , y , txt , size , color , tg):
    """添加粗體文字(畫面,水平位置,垂直位置,大小,顏色,標記)"""
    txt = CANVA.create_text(x, y, text = txt , font = ("Arial", size , "bold") , fill = color , tag = tg)
    return txt

def Result_TXT(CANVA , score, add, ed, times, tag_ADD, tag_Score, tag_Times):
    """顯示結果"""
    CANVA.itemconfig(tag_ADD, text= f"+{add}")
    CANVA.itemconfig(tag_Score, text= f"目前分數：{score}")
    CANVA.itemconfig(tag_Times, text= f"剩餘次數：{times - ed}")


