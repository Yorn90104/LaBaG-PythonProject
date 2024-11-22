import os

#獲取當前資料夾的東西
dir_py_dict = dict()

def extract_py_to_dict(dir_path:str):
    """提取資料夾中的 .py 檔進字典"""
    dir_items = os.listdir(dir_path)
    dir_py_dict[dir_path] = list()
    for item in dir_items:
        if item == os.path.basename(__file__):
            continue   
        if item == "imageb64.py" or item == "soundb64.py":
            continue
        item_path = os.path.join(dir_path, item)
        if os.path.isfile(item_path):
            _, extension = os.path.splitext(item_path) # 使用 splitext 分離文件名與副檔名
            if extension == ".py":
                dir_py_dict[dir_path].append(item)


        if os.path.isdir(item_path):
            if item == ".git":
                continue 
            extract_py_to_dict(item_path) #如果是資料夾就繼續


def py_dict_to_txt(py_files_dict: dict[str, list[str]]):
    with open("PY.txt", 'w', encoding='utf-8') as txt:
        for dir_path in py_files_dict:
            for py_file in py_files_dict[dir_path]:
                txt.write(f"@{dir_path}\\{py_file}\n")
                file_path = os.path.join(dir_path, py_file)
                with open(file_path, "r", encoding='utf-8') as file:
                    txt.write(file.read())
                txt.write("\n\n")


extract_py_to_dict(".")

py_dict_to_txt(dir_py_dict)