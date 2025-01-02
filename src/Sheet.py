#https://script.google.com/macros/s/AKfycbzWA0mMx_B14vrHGW6-QK4tOClSIj1lw7udLJwp7XCg2nZ8hDxt7d-dqnc6WenqBM8FBA/exec

import requests 

class Sheet:
    RawData = list()
    SortedData = dict()
    
    @classmethod
    def GetData(cls):
        """獲取資料"""
        url = "https://script.google.com/macros/s/AKfycbzWA0mMx_B14vrHGW6-QK4tOClSIj1lw7udLJwp7XCg2nZ8hDxt7d-dqnc6WenqBM8FBA/exec"
        cls.RawData = requests.get(url).json()
        cls.SortRawData()

    @classmethod
    def SortRawData(cls):
        """分類整理資料"""
        if cls.RawData:
            del cls.RawData[0] #刪除原始資料的第一個索引 (試算表的欄位名稱)
        for row in cls.RawData : #對每一個的資料(試算表的列位)
            if row:
                del row[0]  #先刪除第一欄的"時間戳記"
                #剩下的資料 [名稱, 分數]
                if row[0] and row[1]: #皆唯「有效的值」
                    name = str(row[0]) #將名稱那格變為字串型態
                    score = int(row[1]) #將分數那格變為整數型態
                    cls.SortedData[name] = max(cls.SortedData.get(name, 0), score) # 原分數與新分數取最大 如果還沒有資料則原分數為0
                    
        print("\n".join([f"{name}: {score}" for name, score in cls.SortedData.items()]))
                    
    @classmethod
    def CommitScore(cls, name: str= None, score: int= 0):
        """提交分數"""
        if name: # 檢查是否是「有效的值」
            if isinstance(score, int) and score >= 0:  # 檢查是否為正整數
                url = f"https://docs.google.com/forms/d/18dVGtPExBUc0p1VbsmMxCyujQoldI6GKQWZQGJQ-yzY/formResponse?entry.582969025={name}&entry.995493130={score}"
                web = requests.get(url)
                if web.status_code == 200:
                    cls.SortedData[name] = max(cls.SortedData.get(name, 0), score)
                    print("資料已上傳")
                else:
                        print(f"錯誤：HTTP狀態碼 {web.status_code}")
            else:
                print("分數無效，必須為正整數！")
        else:
                print("名稱為空，資料未上傳！")

    @classmethod 
    def GetScore(cls, name: str= None):
        """名稱取得分數"""
        if name: # 檢查是否是「有效的值」
            return cls.SortedData.get(name, 0)
        print("名稱無效！")
        return 0
    
    @classmethod
    def RankedData(cls):
        """按分數排名過後的資料"""
        return dict(sorted(cls.SortedData.items(), key=lambda item: item[1], reverse=True)) #.items() 回傳 tuple(key, value)
        

if __name__ == "__main__":
    Sheet.GetData()