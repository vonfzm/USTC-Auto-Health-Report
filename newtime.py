import cv2
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import random,time
import datetime

‘’‘
# 安康
now_str = datetime.datetime.now().strftime('%Y-%m-%d')
now = datetime.datetime.strptime(now_str, "%Y-%m-%d")
past = datetime.datetime.strptime("2021-9-26", "%Y-%m-%d") #接种完成时间
days = (now - past).days

bk_img = cv2.imread("akm.jpg")
font1 = ImageFont.truetype("arialbold.ttf", 58)# 安康码时间字体大小
font2 = ImageFont.truetype("Arial Unicode.ttf", 38)# 接种疫苗天数字体大小
img_pil = Image.fromarray(bk_img)
draw = ImageDraw.Draw(img_pil)
#绘制文字信息
draw.text((270, 920), time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), (0, 0, 0), font1)# 安康码时间位置
draw.text((705, 783), str(days), (0, 0, 0), font2)# 接种疫苗天数位置
bk_img = np.array(img_pil)

cv2.imwrite("Screenshot_Alipay.jpg",bk_img)

time.sleep(random.randint(7, 13))
’‘’

# 行程
bk_img = cv2.imread("xcm.jpg")
font = ImageFont.truetype("Arial Unicode.ttf", 38)# 行程码时间字体大小
img_pil = Image.fromarray(bk_img)
draw = ImageDraw.Draw(img_pil)
#绘制文字信息
draw.text((435, 690), time.strftime("%Y.%m.%d %H:%M:%S", time.localtime()), (150, 150, 150), font)# 行程码时间位置
bk_img = np.array(img_pil)

cv2.imwrite("Screenshot_Wechat.jpg",bk_img)

