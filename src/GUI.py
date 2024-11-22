import tkinter as tk
from PIL import Image, ImageTk
import base64
from io import BytesIO
import os
import time
import wave
import tempfile
from pygame import mixer
mixer.init()

temp_files = []

#region 視窗區
def setup_tk_win(name, icon_file_path: str,  width: int, height: int):
    """設置 tkinter 視窗(視窗名, 視窗圖標檔案路徑, 寬, 高)"""
    win = tk.Tk()
    win.title(name)
    if icon_file_path != None:
        win.iconbitmap(icon_file_path) #視窗圖標.ico
    
    if width != None and height != None:
        width = width
        height = height

    win.geometry(f"{width}x{height}")
    win.resizable(False, False)

    def clean_temp():
        """關閉視窗時刪除臨時 圖標 & 音訊文件"""
        win.destroy()
        stop_music()
        mixer.quit() 
        if os.path.exists("temp_icon.ico"):
            os.remove("temp_icon.ico")
        for temp_file in temp_files:
            if os.path.exists(temp_file):
                try:
                    os.remove(temp_file)
                except PermissionError:
                    time.sleep(1)
                    try:
                        os.remove(temp_file)
                    except PermissionError:
                        print(f"仍然無法刪除：{temp_file}")
                

    win.protocol("WM_DELETE_WINDOW", clean_temp)#綁定關閉視窗

    return win

def setup_frame_and_canvas(win, w, h, BG_pic: ImageTk.PhotoImage):
    """創建 & 設置畫面(視窗, 寬度, 高度, 背景圖片)"""
    Frame = tk.Frame(win, width= w, height= h, bg='lightblue')
    Canvas = tk.Canvas(Frame, width=w, height= h)
    Canvas.pack(fill="both", expand=True)
    Canvas.create_image(0, 0, image = BG_pic, anchor="nw", tag= "BG")
    return Frame, Canvas

def switch_frame(frame1: tk.Frame, frame2: tk.Frame):
    """切換畫面(畫面1 to 畫面2)"""
    frame1.pack_forget()
    frame2.pack(fill='both', expand=True)

def init_window_mainloop(win:tk.Tk, frame):
    """顯示初始畫面並運行 Tkinter 主循环"""
    frame.pack(fill='both', expand=True)
    win.mainloop()


#endregion

#region 圖像元素區

def process_image_path(file_path: str, width: int= 0, height: int= 0):
        """處理成TK可識別的圖 (圖檔路徑, 長, 寬)"""
        pic = Image.open(file_path).convert("RGBA")
        pic = pic.resize((width, height) , Image.LANCZOS)  # 調整圖片大小
        picture = ImageTk.PhotoImage(pic)
        return picture
def load_picture(CANVA: tk.Canvas, picture: ImageTk.PhotoImage, x: int = 0, y: int = 0 , tg: str = ""):
        """加載新的圖片並放在CANVA上 (畫面 , 照片, 水平座標, 垂直座標, 標記)"""
        CANVA.create_image(x, y, image = picture, anchor = "nw" , tag = tg)

def update_picture(CANVA: tk.Canvas, tg: str, picture: ImageTk.PhotoImage) :
    """更換CANVA上的圖片 (畫面, 標記, 圖)"""
    CANVA.itemconfig(tg , image = picture)

def add_text(CANVA: tk.Canvas, txt: str, x: int = 0, y: int = 0, size: int = 12, color: str = "white" , tg: str = "", align: str = "center"):
    """添加粗體文字(畫面, 文字, 水平位置, 垂直位置, 大小, 顏色, 標記, 對齊方式[東南西北])"""
    CANVA.create_text(
                    x, y,
                    text = txt ,
                    font = ("Arial", size , "bold") ,
                    fill = color ,
                    tag = tg,
                    anchor = align
                    )

def txt_button(win, CMD , txt: str, w: int, h: int, x: int = 0, y: int = 0, size: int = 12, font_color: str = "black", bg_color: str = "white"):
    """添加粗體文字按鈕(win, 執行動作, 文字, 按鈕寬度, 按鈕高度, 水平位置, 垂直位置, 文字大小, 文字顏色, 背景顏色)！！全部畫面！！"""
    but = tk.Button(
                    win,
                    text = txt ,
                    command = CMD,
                    font = ("Arial", size, "bold"),
                    fg = font_color,
                    bg = bg_color
                            )
    # 按钮的位置&像素大小
    but.place(x= x, y= y, width=w, height=h)
    return but

def image_button(win,  CMD , CANVA: tk.Canvas, picture: ImageTk.PhotoImage, x: int = 0, y: int = 0, rel: str = "raised", highlight: int = 1):
    """添加圖片按鈕(win, 執行動作, 畫面, 水平座標, 垂直座標, 三圍邊框效果, 焦點邊框厚度)"""
    button = tk.Button(
                    win,
                    image = picture,
                    command = CMD,
                    relief =  rel,
                    highlightthickness = highlight
                    )
    CANVA.create_window(x , y , window = button)
    return button

def delete_button(botton:tk.Button):
    """删除按钮"""
    botton.destroy()

def input_box(win, CANVA: tk.Canvas ,txt: str ="",x: int = 0, y: int = 0, size: int = 16, width: int = 12) :
    """文字輸入盒(視窗,畫面,提示文字,水平座標,垂直座標,文字大小,寬度)"""
    entry = tk.Entry(win, width = width, font=("Arial", size))
    entry.insert(0, txt) 
    CANVA.create_window(x, y, window = entry)
    return entry

def get_input(input_box:tk.Entry):
    """獲取文字輸入盒內容"""
    user_input = input_box.get()
    content = str(user_input.strip()) #去除字串前後空白
    return content

def reset_input_box(input_box:tk.Entry, content: str = ""):
    """重新載入輸入盒內容"""
    input_box.delete(0, "end")
    input_box.insert(0, content)

#region base64區

def encode_image(files: list):
    """產生base64編碼的圖像字典檔"""
    image_dict = dict()
    for file in files:
        with open(f".\\Asset\\{file}", mode = "rb") as f :
            image_b64 = base64.b64encode(f.read())
        image_dict[file.split(".")[0]] = image_b64
    with open((f".\\src\\imageb64.py"), mode = "w") as f:
        f.write("image_dict =")
        f.write(image_dict.__repr__())

def process_image_base64(image_dict: dict, name: str, width: int= 0, height: int= 0):
    """處理成TK可識別的圖 (圖像字典,名稱, 長, 寬)【base64】"""
    decode_pic = base64.b64decode(image_dict[name])
    pic = Image.open(BytesIO(decode_pic))
    pic = pic.resize((width, height) , Image.LANCZOS)  # 調整圖片大小
    picture = ImageTk.PhotoImage(pic)
    return picture

def save_icon(image_dict: dict, name: str):
    """創建並保存臨時圖標《temp_icon.ico》"""
    icon_data = base64.b64decode(image_dict[name])
    with open("temp_icon.ico", "wb") as icon_file:
        icon_file.write(icon_data)

#endregion

#endregion

#region 音訊區

def play_music( file: str, volume: float = 1):
    """播放音樂(音訊檔)"""
    mixer.music.load(file) # 背景音樂文件
    mixer.music.set_volume(volume)
    mixer.music.play(-1) # -1 參數表示循環播放

def stop_music():
    """停止當前音樂"""
    mixer.music.stop()

def switch_music(bgm_playing, file: str, game_running = True) :
    """切換音樂(音訊檔)"""
    if bgm_playing:
        stop_music()
        if game_running:
            play_music(file)

def play_sound(sound: mixer.Sound, volume: float = 1):
    """播放音效(Sound音訊, 音量)"""
    sound.set_volume(volume)
    sound.play()  # 播放音效


#region base64區
def encode_wav(files: list):
    """產生base64編碼的音訊字典檔"""
    sounds = dict()
    for file in files:
        with open(f'.\\Asset\\{file}', mode = 'rb') as f:
            sound_b64 = base64.b64encode(f.read())
        sounds[file.split('.')[0]] = sound_b64
    with open(f'.\\src\\soundb64.py', mode='w') as f:
        f.write("wav_dict =")
        f.write(sounds.__repr__())

def decode_sound(wav_dict: dict, name):
    # 解碼 base64 音頻數據
    binary_data = base64.b64decode(wav_dict[name])
    # 將二進制數據讀取到 BytesIO 中
    audio_data = BytesIO(binary_data)

    # 讀取 WAV 數據
    with wave.open(audio_data, 'rb') as wav_file:
        params = wav_file.getparams()
        frames = wav_file.readframes(params.nframes)

    # 創建一個 Sound 對象
    sound = mixer.Sound(buffer=frames)
    return sound

def decode_music(wav_dict: dict, name):
    # 解碼 base64 音頻數據
    binary_data = base64.b64decode(wav_dict[name])
    # 將二進制數據讀取到 BytesIO 中
    audio_data = BytesIO(binary_data)

    # 讀取 WAV 數據
    with wave.open(audio_data, 'rb') as wav_file:
        params = wav_file.getparams()
        frames = wav_file.readframes(params.nframes)

    # 轉換為臨時音訊文件
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_file:
        with wave.open(temp_file.name, 'wb') as temp_wav_file:
                temp_wav_file.setparams(params)
                temp_wav_file.writeframes(frames)
                temp_filename = temp_file.name
                temp_files.append(temp_filename)
        
    # 返回臨時文件名
    return temp_filename

#endregion

#endregion