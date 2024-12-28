from GUI import Picture, Audio 
from src.imageb64 import image_dict
from src.soundb64 import wav_dict
try:
    music = Audio()
    music.decode_music(wav_dict, "bgm", "SuperMusic", "GreenMusic", "KachuMusic")
    music.decode_sound(wav_dict, "Ding", "SuperUP", 'GreenUP')

    BG = Picture.process_image_base64(image_dict, "BG", 450, 800)
    SuperCircle = Picture.process_image_base64(image_dict, "SuperCircle", 350, 350)
    Title = Picture.process_image_base64(image_dict, "Title", 450, 253)
    QST = Picture.process_image_base64(image_dict, "QST", 150, 200)

    back = Picture.process_image_base64(image_dict, "back", 30, 30)
    BeginPIC = Picture.process_image_base64(image_dict, "BeginPIC", 150, 50)
    AgainPIC = Picture.process_image_base64(image_dict,'AgainPIC' , 150 , 50)
    SB = Picture.process_image_base64(image_dict,'SB' , 450 , 169) #分數計算方式面板

    Gss = Picture.process_image_base64(image_dict, "Gss", 150, 200)
    Hhh = Picture.process_image_base64(image_dict, "Hhh", 150, 200)
    Hentai = Picture.process_image_base64(image_dict, "Hentai", 150, 200)
    Handsun = Picture.process_image_base64(image_dict, "Handsun", 150, 200)
    Kachu = Picture.process_image_base64(image_dict, "Kachu", 150, 200)
    Rrr = Picture.process_image_base64(image_dict, "RRR", 150, 200)

    #region 超級阿禾區
    SuperBG = Picture.process_image_base64(image_dict,'SuperBG' , 450 , 800)
    SuperTitle = Picture.process_image_base64(image_dict,'SuperTitle' , 450 , 253)
    SuperQST = Picture.process_image_base64(image_dict,"SuperQST" , 150 , 200)
    SuperPOP = Picture.process_image_base64(image_dict,'SuperPOP' , 450 , 800)
    super_hhh = Picture.process_image_base64(image_dict,'super_hhh' , 150 , 200)
    #endregion

    #region 綠光阿瑋區
    GreenBG = Picture.process_image_base64(image_dict,'GreenBG' , 450 , 800)
    GreenTitle = Picture.process_image_base64(image_dict,'GreenTitle' , 450 , 253)
    GreenQST = Picture.process_image_base64(image_dict,"GreenQST" , 150 , 200)
    GreenPOP = Picture.process_image_base64(image_dict,'GreenPOP' , 450 , 800)
    
    GreenLeft = Picture.process_image_base64(image_dict,'GreenLeft' , 150 , 200)
    GreenMid = Picture.process_image_base64(image_dict,'GreenMid' , 150 , 200)
    GreenRight = Picture.process_image_base64(image_dict,'GreenRight' , 150 , 200)

    green_wei = Picture.process_image_base64(image_dict,'green_wei' , 150 , 200)

    #endregion
    #region 皮卡丘充電區
    KachuBG = Picture.process_image_base64(image_dict,'KachuBG' , 450 , 800)
    KachuTitle = Picture.process_image_base64(image_dict,'KachuTitle' , 450 , 253)
    KachuQST = Picture.process_image_base64(image_dict,"KachuQST" , 150 , 200)
    KachuPOP = Picture.process_image_base64(image_dict,'KachuPOP' , 450 , 800)
    pikachu = Picture.process_image_base64(image_dict,'pikachu' , 150 , 200)
    
    #endregion
except Exception as e:
    print(e)