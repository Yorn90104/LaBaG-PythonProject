import logging
from typing import Union
import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk
import base64
from io import BytesIO
import os
import wave
import tempfile
from pygame import mixer

# 設置基本日誌配置
logging.basicConfig(
    level=logging.DEBUG,  # 設置最低日誌級別（DEBUG, INFO, WARNING, ERROR, CRITICAL）
    format='%(asctime)s - %(levelname)s - %(message)s',  # 設置日誌格式
    handlers=[
        logging.StreamHandler()  # 只输出到控制台
    ]
)

class BaseWindow():
    """基本視窗類"""
    def __init__(self, title: str = None, width: int = 300, height: int = 300):
        self.window_title = title
        self.width = width
        self.height = height

        self.__frame_dict = dict()
        self.__canvas_dict = dict()
        self.__button_dict = dict()
        self.__entry_dict = dict()
        self.__subwindow_dict = dict()
    
    def Canva(self, canvas_name: str= None) -> tk.Canvas:
        "使用 Tkinter.Canvas 相關操作"
        if canvas_name in self.__canvas_dict:
            return self.__canvas_dict[canvas_name]
        else:
            raise KeyError(f"無法從 {type(self).__name__}.__canvas_dict 找到名為 {canvas_name} 的canvas")

    def Frame(self, frame_name: str= None) -> tk.Frame:
        "使用 Tkinter.Frame 相關操作"
        if frame_name in self.__frame_dict:
            return self.__frame_dict[frame_name]
        else:
            raise KeyError(f"無法從 {type(self).__name__}.__frame_dict 找到名為 {frame_name} 的frame")

    def Button(self, button_name: str= None) -> tk.Button:
        "使用 Tkinter.Button 相關操作"
        if button_name in self.__button_dict:
            return self.__button_dict[button_name]
        else:
            raise KeyError(f"無法從 {type(self).__name__}.__button_dict 找到名為 {button_name} 的button")
        
    def Entry(self, entry_name: str= None) -> tk.Entry:
        """使用 Tkinter.Entry 相關操作"""
        if entry_name in self.__entry_dict:
            return self.__entry_dict[entry_name]
        else:
            raise KeyError(f"無法從 {type(self).__name__}.__entry_dict 找到名為 {entry_name} 的entry")
    
    def SubWindow(self, window_name: str = None) -> "SubWindow": #延遲解析
        """使用 SubWindow (Tkinter.Toplevel) 相關操作"""
        if window_name in self.__subwindow_dict:
            return self.__subwindow_dict[window_name]
        else:
            raise KeyError(f"無法從 {type(self).__name__}._subwindow_dict 找到名為 {window_name} 的subwindow")
    
    def setup_frame_and_canvas(self, name,  BG_pic: ImageTk.PhotoImage = None):
        """創建 & 設置畫面(畫面名稱, 背景圖片)"""
        Frame = tk.Frame(self, width= self.width, height= self.height, bg='lightblue')
        Canvas = tk.Canvas(Frame, width= self.width, height= self.height)
        Canvas.pack(fill="both", expand=True)
        Canvas.create_image(0, 0, image = BG_pic, anchor="nw", tag= "BG")
        self.__frame_dict[name] = Frame
        self.__canvas_dict[name] = Canvas

    def switch_frame(self, frame1_name: str, frame2_name: str):
        """切換畫面(畫面1 to 畫面2)"""
        self.Frame(frame1_name).pack_forget()
        self.Frame(frame2_name).pack(fill='both', expand=True)

    def first_window(self, frame_name: str):
        """顯示首個畫面"""
        self.Frame(frame_name).pack(fill='both', expand=True)

    def load_picture(self, canvas_name: str = None, img: ImageTk.PhotoImage = None, x: int = 0, y: int = 0 , tg: str = ""):
        """加載新的圖片並放在CANVA上 (畫面 , 照片, 水平座標, 垂直座標, 標記)"""
        self.Canva(canvas_name).create_image(x, y, image = img, anchor = "nw" , tag = tg)
    
    def add_text(self, canvas_name: str = None, txt: str = "", x: int = 0, y: int = 0, size: int = 12, color: str = "white" , tg: str = "", align: str = "center"):
        """添加粗體文字(畫面, 文字, 水平位置, 垂直位置, 大小, 顏色, 標記, 對齊方式[東南西北])"""
        self.Canva(canvas_name).create_text(
                        x, y,
                        text = txt ,
                        font = ("Arial", size , "bold") ,
                        fill = color ,
                        tag = tg,
                        anchor = align
                        )

    def update_by_tag(self, canvas_name: str = None, tg: str = "", new_item: Union[str, ImageTk.PhotoImage, None] = None) -> None:
        """根據標記(tag)更換 CANVA 上的 物件 (畫面, 標記, 新物件)"""
        canva = self.Canva(canvas_name)

        if isinstance(new_item, str):
            canva.itemconfig(tg, text=new_item)
        elif isinstance(new_item, ImageTk.PhotoImage):
            canva.itemconfig(tg, image=new_item)
        elif new_item is not None:
            raise TypeError(f"不支援的類型: {type(new_item)}，請傳入 str 或 ImageTk.PhotoImage")

    def delete_canvas_tag(self, canvas_name: str = None, tg: str = ""):
        """根據標記刪除CANVA上的物件 (畫面, 標記)"""
        self.Canva(canvas_name).delete(tg)

    def message_box(self, message: str = ""):
        """顯示訊息框"""
        messagebox.showinfo(self.window_title, message)
        
    def image_button(self, button_name: str, CMD, canvas_name: str = None, img: ImageTk.PhotoImage = None, x: int = 0, y: int = 0, rel: str = "raised", highlight: int = 1):
        """添加圖片按鈕(按鈕名, 執行動作, 畫面名, 圖片, 水平座標, 垂直座標, 三圍邊框效果, 焦點邊框厚度)"""
        button = tk.Button(
                        self,
                        image = img,
                        command = CMD,
                        relief =  rel,
                        highlightthickness = highlight
                        )
        self.Canva(canvas_name).create_window(x , y , window = button, tags= button_name)
        self.__button_dict[button_name] = button

    def txt_button(self, button_name: str, CMD  ,canvas_name: str = None,  txt: str = None, w: int= 0, h: int= 0, x: int = 0, y: int = 0, size: int = 12, font_color: str = "black", bg_color: str = "white"):
        """添加粗體文字按鈕(按鈕名, 執行動作, 畫面名, 文字, 按鈕寬度, 按鈕高度, 水平位置, 垂直位置, 文字大小, 文字顏色, 背景顏色)"""
        button = tk.Button(
                        self,
                        text = txt ,
                        command = CMD,
                        font = ("Arial", size, "bold"),
                        fg = font_color,
                        bg = bg_color
                                )
        # 按钮的像素大小&位置
        button.place(width=w, height=h)
        self.Canva(canvas_name).create_window(x , y , window = button, tags= button_name)
        self.__button_dict[button_name] = button

    def delete_button(self, button_name: str):
        """刪除按鈕"""
        self.Button(button_name).destroy()

    def input_box(self, canvas_name: str = None, entry_name: str= None,txt: str ="",x: int = 0, y: int = 0, size: int = 16, width: int = 12) :
        """文字輸入盒(畫面名, 輸入盒名稱, 提示文字,水平座標,垂直座標,文字大小,寬度)"""
        entry = tk.Entry(self, width = width, font=("Arial", size))
        entry.insert(0, txt) 
        self.Canva(canvas_name).create_window(x, y, window = entry)
        self.__entry_dict[entry_name] = entry

    def get_input(self, entry_name: str= None):
        """獲取文字輸入盒內容"""
        return self.Entry(entry_name).get().strip() #去除字串前後空白
        
    
    def reset_input_box(self, entry_name: str= None, content: str = ""):
        """重新載入輸入盒內容"""
        self.Entry(entry_name).delete(0, "end")
        self.Entry(entry_name).insert(0, content)
    
    def open_file(self) -> str:
        """開啟檔案(回傳檔案路徑)"""
        return filedialog.askopenfilename()

class Window(tk.Tk, BaseWindow):
    def __init__(self, title: str = None, width: int = 300, height: int = 300):
        """主視窗類別 (視窗名稱, 寬, 高)"""
        tk.Tk.__init__(self)  # 初始化 tk.Tk
        BaseWindow.__init__(self, title, width, height)  # 初始化 BaseWindow
        mixer.init() # 初始化音訊
        self.title(self.window_title)
        self.geometry(f"{self.width}x{self.height}")
        self.resizable(False, False) # 鎖定視窗大小
        
        self.temp_files = list() #臨時文件

        self.protocol("WM_DELETE_WINDOW", self.clean_temp) #綁定關閉視窗

    def clean_temp(self):
        """關閉視窗時刪除臨時 圖標 & 音訊文件"""
        logging.debug("正在關閉視窗")
        self.destroy()
        mixer.music.stop()
        mixer.quit() 
        if os.path.exists("temp_icon.ico"):
            os.remove("temp_icon.ico")
            logging.debug(f"已成功刪除臨時文件: temp_icon.ico")
        
        for temp_file in self.temp_files:
            if os.path.exists(temp_file):
                try:
                    os.remove(temp_file)
                    logging.debug(f"已成功刪除臨時文件: {temp_file}")
                except Exception as e:
                    logging.error(f"無法刪除臨時文件: {temp_file}, 原因: {e}")

    def save_icon_use(self, image_dict: dict, name: str):
        """創建、保存並使用臨時圖標《temp_icon.ico》"""
        icon_data = base64.b64decode(image_dict[name])
        with open("temp_icon.ico", "wb") as icon_file:
            icon_file.write(icon_data)
        self.iconbitmap("temp_icon.ico") #視窗圖標.ico

class SubWindow(tk.Toplevel, BaseWindow):
    """子視窗類"""
    def __init__(self, master :tk.Tk = None, title: str = None, width: int = 300, height: int = 300, BG_pic: ImageTk.PhotoImage = None):
        """子視窗類別 (父視窗, 子視窗名稱, 寬, 高)"""
        tk.Toplevel.__init__(self, master)  # 初始化 tk.Toplevel
        BaseWindow.__init__(self, title, width, height)  # 初始化 BaseWindow
        self.master = master
        self.iconbitmap(self.master.iconbitmap())
        
        self.title(self.master.title())
        if title is not None:
            self.title(title)

        self.geometry(f"{self.width}x{self.height}")
        self.resizable(False, False)  # 鎖定視窗大小

        self.setup_frame_and_canvas("Main", BG_pic)
        self.first_window("Main")
    
    def load_picture(self, img: ImageTk.PhotoImage = None, x: int = 0, y: int = 0 , tg: str = ""):
        """加載新的圖片並放在CANVA上 (照片, 水平座標, 垂直座標, 標記)"""
        super().load_picture("Main", img, x, y, tg)
    
    def add_text(self, txt: str = "", x: int = 0, y: int = 0, size: int = 12, color: str = "white" , tg: str = "", align: str = "center"):
        """添加粗體文字(文字, 水平位置, 垂直位置, 大小, 顏色, 標記, 對齊方式[東南西北])"""
        super().add_text("Main", txt, x, y, size, color, tg, align)

    def update_by_tag(self, tg: str = "", new_item: Union[str, ImageTk.PhotoImage, None] = None) -> None:
        """根據標記(tag)更換 CANVA 上的 物件 (標記, 新物件)"""
        super().update_by_tag("Main", tg, new_item)

    def delete_canvas_tag(self, tg: str = ""):
        """根據標記刪除CANVA上的物件 (標記)"""
        super().delete_canvas_tag("Main", tg)

    def message_text(self,ms: int = 1000, txt: str = "", x: int = 0, y: int = 0, size: int = 12, color: str = "white" , align: str = "center"):
        """顯示短暫訊息文字(ms毫秒: 預設 1000)"""
        self.add_text(txt, x, y, size, color, "msg", align)
        self.master.after(ms, lambda:self.delete_canvas_tag("msg"))

    def image_button(self, button_name: str, CMD, img: ImageTk.PhotoImage = None, x: int = 0, y: int = 0, rel: str = "raised", highlight: int = 1):
        super().image_button(button_name, CMD, "Main", img, x, y, rel, highlight)
    
    def txt_button(self, button_name: str, CMD, txt: str = None, w: int= 0, h: int= 0, x: int = 0, y: int = 0, size: int = 12, font_color: str = "black", bg_color: str = "white"):
        super().txt_button(button_name, CMD, "Main", txt, w, h, x, y, size, font_color, bg_color)

    def input_box(self, entry_name: str= None, txt: str = "", x: int = 0, y: int = 0, size: int = 16, width: int = 12):
        super().input_box("Main", entry_name, txt, x, y, size, width)

    def setup_subwindow(self, window_name: str = None,  width: int = 300, height: int= 300, BG_pic: ImageTk.PhotoImage = None):
        """建立子視窗(視窗, 寬, 高)"""
        sw = SubWindow(self, window_name, width, height, BG_pic)
        self.__subwindow_dict[window_name] = sw

class Picture:
    @staticmethod
    def process_image_base64(image_dict: dict, name: str, width: int= 0, height: int= 0):
        """處理成TK可識別的圖 (圖像字典, 名稱, 長, 寬)"""
        if name in image_dict:
            decode_pic = base64.b64decode(image_dict[name])
            pic = Image.open(BytesIO(decode_pic))
            pic = pic.resize((width, height) , Image.LANCZOS)  # 調整圖片大小
            picture = ImageTk.PhotoImage(pic)
            return picture
        else :
            raise KeyError(f"無法從 image_dict 找到名為 {name} 的圖片")

class Audio:
    def __init__(self):
        self.bgm_playing = False
        self.sound_dict = dict()
        self.music_dict = dict()
        self.temp_files = list() #要與 Windows.temp_files 做連結
    
    def Sound(self, sound_name: str= None) -> mixer.Sound:
        """使用 Pygame.mixer.Sound 相關操作"""
        return self.sound_dict[sound_name]

    def play_music(self, music_name: str = None, volume: float = 1, loops: int = -1):
        """播放音樂"""
        mixer.music.load(self.music_dict[music_name]) # 背景音樂文件
        mixer.music.set_volume(volume)
        mixer.music.play(loops) # -1 參數表示循環播放
        self.bgm_playing = True

    def stop_music(self):
        """停止當前音樂"""
        mixer.music.stop()
        self.bgm_playing = False

    def switch_music(self, music_name: str = None, game_running = True) :
        """切換音樂"""
        if self.bgm_playing:
            self.stop_music()
            if game_running:
                self.play_music(music_name)

    def play_sound(self, sound_name: str= None, volume: float = 1):
        """播放音效(Sound音訊, 音量)"""
        sound = self.Sound(sound_name)
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
            

    def decode_music(self,  wav_dict: dict, *names):
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
                            self.temp_files.append(temp_filename)
                    
                # 儲存臨時文件名
                logging.debug(f"成功創建臨時文件: {temp_filename}")
                self.music_dict[name] = temp_filename
            except Exception as e:
               logging.error(f"音樂解碼失敗 ({name}): {e}")
    #endregion