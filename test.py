data = {
    "36": {
        "RandNums[0]": 4,
        "RandNums[1]": 3,
        "RandNums[2]": 2,
        "SuperHHH": 17,
        "GreenWei": 3
    },
    "37": {
        "RandNums[0]": 98,
        "RandNums[1]": 99,
        "RandNums[2]": 100,
        "SuperHHH": 17,
        "GreenWei": 3
    },
    "38": {
        "RandNums[0]": 58,
        "RandNums[1]": 59,
        "RandNums[2]": 60,
        "SuperHHH": 10,
        "GreenWei": 3
    },
    "39": {
        "RandNums[0]": 98,
        "RandNums[1]": 99,
        "RandNums[2]": 100,
        "SuperHHH": 17,
        "GreenWei": 3
    },
    "40": {
        "RandNums[0]": 78,
        "RandNums[1]": 79,
        "RandNums[2]": 80,
        "SuperHHH": 17,
        "GreenWei": 3
    },
    "41": {
        "RandNums[0]": 4,
        "RandNums[1]": 3,
        "RandNums[2]": 2,
        "SuperHHH": 17,
        "GreenWei": 3
    },
    "42": {
        "RandNums[0]": 98,
        "RandNums[1]": 99,
        "RandNums[2]": 100,
        "SuperHHH": 17,
        "GreenWei": 3
    },
    "43": {
        "RandNums[0]": 58,
        "RandNums[1]": 59,
        "RandNums[2]": 60,
        "SuperHHH": 10,
        "GreenWei": 3
    },
    "44": {
        "RandNums[0]": 98,
        "RandNums[1]": 99,
        "RandNums[2]": 100,
        "SuperHHH": 17,
        "GreenWei": 3
    },
    "45": {
        "RandNums[0]": 78,
        "RandNums[1]": 79,
        "RandNums[2]": 80,
        "SuperHHH": 17,
        "GreenWei": 3
    },
    "46": {
        "RandNums[0]": 4,
        "RandNums[1]": 3,
        "RandNums[2]": 2,
        "SuperHHH": 17,
        "GreenWei": 3
    },
    "47": {
        "RandNums[0]": 98,
        "RandNums[1]": 99,
        "RandNums[2]": 100,
        "SuperHHH": 17,
        "GreenWei": 3
    },
    "48": {
        "RandNums[0]": 58,
        "RandNums[1]": 59,
        "RandNums[2]": 60,
        "SuperHHH": 10,
        "GreenWei": 3
    },
    "49": {
        "RandNums[0]": 98,
        "RandNums[1]": 99,
        "RandNums[2]": 100,
        "SuperHHH": 17,
        "GreenWei": 3
    },
    "50": {
        "RandNums[0]": 78,
        "RandNums[1]": 79,
        "RandNums[2]": 80,
        "SuperHHH": 17,
        "GreenWei": 3
    }
}

# 修改鍵值 "36" 到 "50" 為 "51" 到 "65"
updated_data = {}
for key, value in data.items():
    new_key = str(int(key) + 15)  # 將鍵的值增加 15
    updated_data[new_key] = value

print(updated_data)