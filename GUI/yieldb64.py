import os
import base64

#產生 base64 音訊與圖像
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

sort_item(asset_dir_items)

encode_image(images)
encode_wav(sounds)
