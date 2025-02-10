import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.title("")
root.geometry('200x200')

def show():
    file_path = filedialog.askopenfilename()   # 選擇檔案後回傳檔案路徑與名稱
    print(file_path)                           # 印出路徑

# Button 設定 command 參數，點擊按鈕時執行 show 函式
btn = tk.Button(root,
                text='開啟檔案',
                font=('Arial',20,'bold'),
                command=show
              )
btn.pack()

root.mainloop()