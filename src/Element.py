from src.GUI import process_image_base64, decode_sound, decode_music
from src.imageb64 import image_dict
from src.soundb64 import wav_dict

BG = process_image_base64(image_dict,'BG' , 450 , 800)
Title = process_image_base64(image_dict,'Title' , 450 , 253)
QST = process_image_base64(image_dict,'QST' , 150 , 200)  # ?


gss = process_image_base64(image_dict,'Gss' , 150 , 200)  # A
hhh = process_image_base64(image_dict,'Hhh' , 150 , 200)  # B
hentai = process_image_base64(image_dict,'Hentai' , 150 , 200)  # C
handsun = process_image_base64(image_dict,'Handsun' , 150 , 200)  # D
kachu = process_image_base64(image_dict,'Kachu' , 150 , 200)  # E
rrr = process_image_base64(image_dict,'RRR' , 150 , 200)  # F


BeginPIC = process_image_base64(image_dict,'BeginPIC' , 150 , 50)
AgainPIC = process_image_base64(image_dict,'AgainPIC' , 150 , 50)
SB = process_image_base64(image_dict,'SB' , 450 , 169) #記分板
back = process_image_base64(image_dict,'back' , 30 , 30) #返回

Ding = decode_sound(wav_dict, 'Ding')

#region 超級阿禾區

SuperCircle = process_image_base64(image_dict,'SuperCircle' , 350 , 350)

SuperBG = process_image_base64(image_dict,'SuperBG' , 450 , 800)
SuperTitle = process_image_base64(image_dict,'SuperTitle' , 450 , 253)
SuperQST = process_image_base64(image_dict,'SuperQST' , 150 , 200)
SuperPOP = process_image_base64(image_dict,'SuperPOP' , 450 , 800)

super_hhh = process_image_base64(image_dict,'super_hhh' , 150 , 200)

SuperUP = decode_sound(wav_dict, 'SuperUP')

   


#endregion

#region 綠光阿瑋區

GreenBG = process_image_base64(image_dict,'GreenBG' , 450 , 800)
GreenTitle = process_image_base64(image_dict,'GreenTitle' , 450 , 253)
GreenQST = process_image_base64(image_dict,'GreenQST' , 150 , 200)
GreenPOP = process_image_base64(image_dict,'GreenPOP' , 450 , 800)

GreenLeft = process_image_base64(image_dict,'GreenLeft' , 150 , 200)
GreenMid = process_image_base64(image_dict,'GreenMid' , 150 , 200)
GreenRight = process_image_base64(image_dict,'GreenRight' , 150 , 200)

green_wei = process_image_base64(image_dict,'green_wei' , 150 , 200)

GreenUP = decode_sound(wav_dict, 'GreenUP')
#endregion

#region 皮卡丘充電區

KachuBG = process_image_base64(image_dict,'KachuBG' , 450 , 800)
KachuTitle = process_image_base64(image_dict,'KachuTitle' , 450 , 253)
KachuQST = process_image_base64(image_dict,'KachuQST' , 150 , 200)
KachuPOP = process_image_base64(image_dict,'KachuPOP' , 450 , 800)

pikachu = process_image_base64(image_dict,'pikachu' , 150 , 200)

#endregion

bgm = decode_music(wav_dict, "bgm")
SuperMusic = decode_music(wav_dict, "SuperMusic")
GreenMusic = decode_music(wav_dict, "GreenMusic")
KachuMusic = decode_music(wav_dict, "KachuMusic")