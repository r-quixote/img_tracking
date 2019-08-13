import numpy as np
import cv2
import os
import matplotlib.pyplot as plt
import pylab as p

def get_ROI(img):
    print("\nuse `space` or `enter` to finish selection")
    print("use `c`     or `Esc`   to cancel selection (function will return zero by zero)")
    cv2.namedWindow("SELECT ROI", cv2.WINDOW_NORMAL) 
#    cv2.moveWindow("SELECT ROI",550,550) #in case it opens in a bad location
    cv2.waitKey(1)
    bbox = cv2.selectROI("SELECT ROI", img, True)
    cv2.destroyWindow("SELECT ROI")
    return bbox
    
def crop(img, x, y, h, w, name):
    """
    shows the croped version of img, and returns it
    img - the image that you want to crop
    name - the window name
    """    
    crop_img = img[y:y+h, x:x+w]
    cv2.namedWindow(name, cv2.WINDOW_NORMAL) 
    cv2.imshow(name, crop_img)
    cv2.waitKey(1)
    return crop_img

def remove_blue(img):
    """
	ment for finding the orange, and yellow fluo colors
	using the H channel only (from HSV)
	"""
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
    lower_red = np.array([135,0,0])
    upper_red = np.array([255,255,255])
    red_mask = cv2.inRange(hsv, lower_red, upper_red)
    
    lower_yellow = np.array([65,0,0])
    upper_yellow = np.array([88,255,255])
    yellow_mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
    
    full_mask = yellow_mask | red_mask # combine both masks ( | = OR )
    
    res = cv2.bitwise_or(img,img, mask= full_mask)
    cv2.namedWindow("no blue", cv2.WINDOW_NORMAL) 
    cv2.imshow("no blue", res)
    return res 

def color_filter(img):
    """
	ment for finding the red
	using the R channel only (from BGR)
	"""
    p.imshow(croped_img[:,:,2], vmin = 0, vmax = 255) ##use this to find the color range!
    
    lower_red = np.array([0,0,105])
    upper_red = np.array([255,255,255])
    red_mask = cv2.inRange(img, lower_red, upper_red)
    
#    
#    lower_blue = np.array([250,0,0])
#    upper_blue = np.array([255,255,255])
#    blue_mask = cv2.inRange(img, lower_blue, upper_blue)
#    
#    nonblue_mask = cv2.bitwise_not(blue_mask)
#    
#    full_mask = nonblue_mask | red_mask
#    
    res = cv2.bitwise_or(img, img, mask = red_mask)
    cv2.namedWindow("no blue", cv2.WINDOW_NORMAL) 
    cv2.imshow("no blue", res)
    return res 
    
#%%
img_path = r"C:\Users\YasmineMnb\Desktop\fluo playing\2_top\DSC_0581.JPG"
img = cv2.imread(img_path)
ROI = get_ROI(img)
croped_img = crop(img, ROI[0], ROI[1], ROI[3], ROI[2], "croped")
#fluo_only  = remove_blue(croped_img)

color_filter(croped_img)
#%%


p.imshow(croped_img[:,:,0], vmin = 0, vmax = 255) ##use this to find the color range!


