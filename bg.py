# -*- coding: utf-8 -*-
# @Author: admin
# @Date:   2017-09-30 11:04:44
# @Last Modified by:   admin
# @Last Modified time: 2017-09-30 17:07:40
import urllib
from urllib import request
import re
import json
import os
from PIL import Image
import win32api,win32con,win32gui
import time

if os.path.exists('D:/SQbgImg') :
	pass
else :
	os.makedirs('D:/SQbgImg')

urlPath = "http://cn.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1"
def getJson(url):
	req = request.Request(url)
	req.add_header(
	    'User-Agent', 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.94 Safari/537.36')
	with request.urlopen(req) as f:
		data =  f.read().decode('utf-8')
		imgurl = json.loads(data)
		url1 = "http://cn.bing.com"
		url2 = imgurl['images'][0]['url']
		x = str(time.time()).replace('.','')
		# dz = urllib.request.urlretrieve(url1+url2,'D:\img\%s.jpg' % x)
		dz = urllib.request.urlretrieve(url1+url2,'D:/SQbgImg/now.jpg')
		return dz[0]

def set_wallpaper_from_bmp(bmp_path):  
	#打开指定注册表路径  
	reg_key = win32api.RegOpenKeyEx(win32con.HKEY_CURRENT_USER,"Control Panel\\Desktop",0,win32con.KEY_SET_VALUE)  
	#最后的参数:2拉伸,0居中,6适应,10填充,0平铺  
	win32api.RegSetValueEx(reg_key, "WallpaperStyle", 0, win32con.REG_SZ, "2")  
	#最后的参数:1表示平铺,拉伸居中等都是0  
	win32api.RegSetValueEx(reg_key, "TileWallpaper", 0, win32con.REG_SZ, "0")  
	#刷新桌面  
	win32gui.SystemParametersInfo(win32con.SPI_SETDESKWALLPAPER,bmp_path, win32con.SPIF_SENDWININICHANGE)  
  
def set_wallpaper(img_path):  
	#把图片格式统一转换成bmp格式,并放在源图片的同一目录  
	img_dir = os.path.dirname(img_path)  
	bmpImage = Image.open(img_path)  
	new_bmp_path = os.path.join(img_dir,'wallpaper.bmp')  
	bmpImage.save(new_bmp_path, "BMP")  
	set_wallpaper_from_bmp(new_bmp_path)  
  
if __name__ == '__main__':  
	a = getJson(urlPath)
	set_wallpaper(a)  
