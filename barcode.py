# -*- coding: utf-8 -*-
import cv2 #ایمپورت کردن opencv
import zbar #ایمپورت کردن zbar
from Tkinter import * #ایمپورت کردن Tkinter (رابط کاربری)
from tkFileDialog   import askopenfilename      #ایمپورت کردن بخش بازکردن فایل (باز کردن عکس از طریق آدرس )
import sys  #ایمپورت کردن sys
def callback(): #ساخت تابع callback
	name= askopenfilename() #ریختن آدرس عکس داخل متغییر
	scanner = zbar.ImageScanner() #تعیین کردن اینکه قرار یه عکس دو بعدی بارکدش خونده بشه
	scanner.parse_config('enable') #پیکربندی برای خوندن رشته
	im = cv2.imread(name)#خواندن عکس از طریق آدرسی که قبلا ریخته شده تو name
	#البته با استفاده از opencv
	
	
	
	gray_im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY) #برای تبدیل رنگ، ما از تابع cv2.cvtColor
	#در اینجا ما تصویر رو grey کردیم یا همون سیاه سفید برای بهتر خوندت بارکد
	
	
	#ریختن سطرها و ستون های های تصویر در متغییر های rows , cols
	rows,cols = im.shape[:2]
	
	#تبدیل کردن تصویر grey شده به باینری برای مشاهده نمونه این لینکو ببیندید 
	#https://docs.opencv.org/3.3.1/d7/d4d/tutorial_py_thresholding.html
	ret,threshold_im = cv2.threshold(gray_im, 150, 255, cv2.THRESH_BINARY)
	
	
	 #cv2.findContours در اینجا ما خطوط را در یک تصویر باینری پیدا می کنیم
	#cv2.CHAIN_APPROX_SIMPLE این contours فشرده می کنه یعنی کلا برای ذخیره حافظه و سبک شدن کار استفاده میشه
	#RETR_EXTERNAL خطوط خارجی رو بازیابی می کند
	im,contours,hierarchy = cv2.findContours(threshold_im, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	
	
#تعریف یک آرایه برای ریختن داده ها از بارکدهای اسکن شده
	scanned_data = {}
	
	
	for contour in contours:
	#پیدا کردن مستطیل چرخیده شده برای پیدا کردن تصویر بارکد های کج شده برای مشاهده یک نمونه تصویر زیر را مشاهده کنید
	#https://docs.opencv.org/3.1.0/boundingrect.png
		rect = cv2.minAreaRect(contour)
		
		
		#انجام محاسبات برای برگرداندن تصویر به حالت قبلی و صاف کردنش 
		w = int(rect[1][0])
		h = int(rect[1][1])
		min_w = cols*0.1
		min_h = rows*0.1
		if w > min_w and h > min_h:
			w_half = int(w*0.5)
			h_half = int(h*0.5)
			center_pt = (int(rect[0][0]), int(rect[0][1]))
			top = center_pt[1] - h_half
			right = center_pt[0] + w_half
			bottom = center_pt[1] + h_half
			left = center_pt[0] - w_half
			angle = int(rect[2])
			
			#تغییر دادن تصویر به مرکز بر اساس پارامترهای که در بالا آورده شده
			M = cv2.getRotationMatrix2D(center_pt, angle, 1)
			
			#در اینجا هم تصویر می چرخه بر اساس ماتریس M و پارامترهای دیگر
			rotated_im = cv2.warpAffine(im.copy(), M, (cols,rows))
			
			#خواندن تصویر با استفاده از zbar 
			zbar_image = zbar.Image(cols, rows, 'Y800', rotated_im.tostring())
			scanner.scan(zbar_image) #اکسن کردن تصویر برای پیدا کردن symbol ها
			for symbol in zbar_image:#داخل حلقست برای اینکه امکان داره چندتا بارکد در یک تصویر باشه
				symbol_type = symbol.type
				symbol_data = symbol.data
				if(symbol_type not in scanned_data.keys()):
					scanned_data[symbol_type] = []
					if symbol_data not in scanned_data[symbol_type]:
						scanned_data[symbol_type].append(symbol_data)
						#پاک کردن تصویر خوانده شده توسط zbar از رم برای سبک تر شدن کار
			del(zbar_image)
			
#اضافه کردن نوع بارکد و داده آن به text در رابط کاربری
	T.insert(END,'بارکد: %s \n' % (scanned_data))
	
#ایجاد tkinter (رابط کاربری)
root = Tk()
#ساخت دکمه و مشخص کردن اینکه پس از کلیک تابع callback اجرا بشه 
Button(text='انتخاب تصویر بارکد', command=callback).pack(fill=X)
#ساخت text با اندازه مشخص  
T = Text(root, height=30, width=100)
T.pack()
#مشخص کردن title فرم
root.title("Barcode Created By Ali Zamani")
mainloop()
