#產生 base64 音訊與圖像
from src.GUI import os, encode_image, encode_wav

asset_dir_items = os.listdir(".\\Asset")

images = list()
sounds = list()

def sort_item(dir_lsit:list):
    for item in dir_lsit:
        item_path = os.path.join(".\\Asset", item)
        _, extension = os.path.splitext(item_path) # 使用 splitext 分離文件名與副檔名
        if extension == ".jpg" or extension == ".png" or extension == ".ico":
            images.append(item)
        elif extension == ".wav":
            sounds.append(item)

sort_item(asset_dir_items)

encode_image(images)
encode_wav(sounds)
