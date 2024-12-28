import tkinter as tk
from PIL import Image, ImageTk
import base64
from io import BytesIO
import os
import wave
import tempfile
from pygame import mixer

class Window(tk.Tk):
    def __init__(self, title: str= "",  width: int = 300, height: int= 300):
        """設置視窗(視窗名, 寬, 高)"""
        super().__init__()
        mixer.init()
        self.title(title)

        
        self.width = width
        self.height = height

        self.geometry(f"{self.width}x{self.height}") #視窗長寬
        self.resizable(False, False) #視窗大小鎖定

        self.frame_dict = dict()
        self.canvas_dict = dict()
        self.button_dict = dict()
        self.entry_dict = dict()
      
        self.temp_files = list() #臨時文件

        self.protocol("WM_DELETE_WINDOW", self.clean_temp)#綁定關閉視窗

    def clean_temp(self):
        """關閉視窗時刪除臨時 圖標 & 音訊文件"""
        self.destroy()
        mixer.music.stop()
        mixer.quit() 
        if os.path.exists("temp_icon.ico"):
            os.remove("temp_icon.ico")
        for temp_file in self.temp_files:
            if os.path.exists(temp_file):
                try:
                    os.remove(temp_file)
                except Exception as e:
                    print(f"無法刪除臨時文件: {temp_file}, 原因: {e}")

    def setup_frame_and_canvas(self, name,  BG_pic: ImageTk.PhotoImage = None):
        """創建 & 設置畫面(畫面名稱, 背景圖片)"""
        Frame = tk.Frame(self, width= self.width, height= self.height, bg='lightblue')
        Canvas = tk.Canvas(Frame, width= self.width, height= self.height)
        Canvas.pack(fill="both", expand=True)
        Canvas.create_image(0, 0, image = BG_pic, anchor="nw", tag= "BG")
        self.frame_dict[name] = Frame
        self.canvas_dict[name] = Canvas
    
    def switch_frame(self, frame1_name: str, frame2_name: str):
        """切換畫面(畫面1 to 畫面2)"""
        if frame1_name in self.frame_dict and frame2_name in self.frame_dict:
            self.frame_dict[frame1_name].pack_forget()
            self.frame_dict[frame2_name].pack(fill='both', expand=True)
        else:
            print(f"切換失敗：畫面 '{frame1_name}' 或 '{frame2_name}' 不存在")

    def init_window_mainloop(self, frame_name: str):
        """顯示初始畫面並運行 Tkinter 主循环"""
        self.frame_dict[frame_name].pack(fill='both', expand=True)
        self.mainloop()

    def save_icon(self, image_dict: dict, name: str):
        """創建並保存臨時圖標《temp_icon.ico》"""
        icon_data = base64.b64decode(image_dict[name])
        with open("temp_icon.ico", "wb") as icon_file:
            icon_file.write(icon_data)
        self.iconbitmap("temp_icon.ico") #視窗圖標.ico


    def load_picture(self, canvas_name: str = None, img: ImageTk.PhotoImage = None, x: int = 0, y: int = 0 , tg: str = ""):
        """加載新的圖片並放在CANVA上 (畫面 , 照片, 水平座標, 垂直座標, 標記)"""
        self.canvas_dict[canvas_name].create_image(x, y, image = img, anchor = "nw" , tag = tg)

    def update_picture(self, canvas_name: str = None,tg: str = "", img: ImageTk.PhotoImage = None) :
        """更換CANVA上的圖片 (畫面, 標記, 圖)"""
        self.canvas_dict[canvas_name].itemconfig(tg , image = img)


    def add_text(self, canvas_name: str = None, txt: str = "", x: int = 0, y: int = 0, size: int = 12, color: str = "white" , tg: str = "", align: str = "center"):
        """添加粗體文字(畫面, 文字, 水平位置, 垂直位置, 大小, 顏色, 標記, 對齊方式[東南西北])"""
        self.canvas_dict[canvas_name].create_text(
                        x, y,
                        text = txt ,
                        font = ("Arial", size , "bold") ,
                        fill = color ,
                        tag = tg,
                        anchor = align
                        )
        
    def image_button(self, button_name: str, CMD, canvas_name: str = None, img: ImageTk.PhotoImage = None, x: int = 0, y: int = 0, rel: str = "raised", highlight: int = 1):
        """添加圖片按鈕(執行動作, 畫面, 水平座標, 垂直座標, 三圍邊框效果, 焦點邊框厚度)"""
        button = tk.Button(
                        self,
                        image = img,
                        command = CMD,
                        relief =  rel,
                        highlightthickness = highlight
                        )
        self.canvas_dict[canvas_name].create_window(x , y , window = button)
        self.button_dict[button_name] = button

    def delete_button(self, button_name: str):
        """刪除按鈕"""
        self.button_dict[button_name].destroy()

    def input_box(self, canvas_name: str = None, entry_name: str= None,txt: str ="",x: int = 0, y: int = 0, size: int = 16, width: int = 12) :
        """文字輸入盒(視窗,畫面,提示文字,水平座標,垂直座標,文字大小,寬度)"""
        entry = tk.Entry(self, width = width, font=("Arial", size))
        entry.insert(0, txt) 
        self.canvas_dict[canvas_name].create_window(x, y, window = entry)
        self.entry_dict[entry_name] = entry

    def get_input(self, entry_name: str= None):
        """獲取文字輸入盒內容"""
        user_input = self.entry_dict[entry_name].get()
        content = str(user_input.strip()) #去除字串前後空白
        return content
    
    def reset_input_box(self, entry_name: str= None, content: str = ""):
        """重新載入輸入盒內容"""
        self.entry_dict[entry_name].delete(0, "end")
        self.entry_dict[entry_name].insert(0, content)

class Image:
    def __init__(self):
        self.image_dict = dict()

    def process_image_base64(self, image_dict: dict, name: str, width: int= 0, height: int= 0):
        """處理成TK可識別的圖 (圖像字典, 名稱, 長, 寬)"""
        decode_pic = base64.b64decode(image_dict[name])
        pic = Image.open(BytesIO(decode_pic))
        pic = pic.resize((width, height) , Image.LANCZOS)  # 調整圖片大小
        picture = ImageTk.PhotoImage(pic)
        self.image_dict[name] = picture

class Audio:
    def __init__(self):
        self.bgm_playing = False
        self.sound_dict = dict()
        self.music_dict = dict()
        

    def play_music(self, music_name: str = None, volume: float = 1, loops: int = -1):
        """播放音樂(音訊檔)"""
        mixer.music.load(self.music_dict[music_name]) # 背景音樂文件
        mixer.music.set_volume(volume)
        mixer.music.play(loops) # -1 參數表示循環播放
        self.bgm_playing = True

    def stop_music(self):
        """停止當前音樂"""
        mixer.music.stop()
        self.bgm_playing = False

    def switch_music(self, file: str, game_running = True) :
        """切換音樂(音訊檔)"""
        if self.bgm_playing:
            self.stop_music()
            if game_running:
                self.play_music(file)

    def play_sound(self, sound: mixer.Sound, volume: float = 1):
        """播放音效(Sound音訊, 音量)"""
        sound.set_volume(volume)
        sound.play()  # 播放音效

    def decode_sound(self, wav_dict: dict, *names):
        """解碼音效"""
        # 解碼 base64 音頻數據
        for name in names:
            binary_data = base64.b64decode(wav_dict[name])
            # 將二進制數據讀取到 BytesIO 中
            audio_data = BytesIO(binary_data)

            # 讀取 WAV 數據
            with wave.open(audio_data, 'rb') as wav_file:
                params = wav_file.getparams()
                frames = wav_file.readframes(params.nframes)

            # 創建一個 Sound 對象
            sound = mixer.Sound(buffer=frames)
            self.sound_dict[name] = sound
            

    def decode_music(self, temp_files: list,  wav_dict: dict, *names):
        """解碼音樂"""
        for name in names:
            try:
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
                    
                # 儲存臨時文件名
                self.music_dict[name] = temp_filename
            except Exception as e:
               print(f"音樂解碼失敗 ({name}): {e}")
    #endregion