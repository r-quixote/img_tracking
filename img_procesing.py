import numpy as np
import cv2
import os
import matplotlib.pyplot as plt
import pylab as p
import traceback
import time
from stat import ST_MTIME

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

def get_orig_path(file_path):
    """
    will only work if both in same directroy:
    "...\8\side_croped" AND "...\8\side"
    """
    try:
        base_folder = file_path.split("_croped")[0]
        cur_file_name = file_path.rsplit("\\",1)[1]
        file_numb = cur_file_name.split("_")[0]
        full_or_file_path = base_folder + "\\DSC_"+ file_numb + ".jpg"

    except IndexError as err:
        traceback.print_tb(err.__traceback__)
        print(err)
        print("check the names of the folders")
        return "EEROR"
    except FileNotFoundError as err:
        traceback.print_tb(err.__traceback__)
        print(err)
        print("check the names of the folders")
        return "EEROR"
    return full_or_file_path

def get_time(file_path):
    if "CROPED" in file_path:
        file_path = get_orig_path(file_path)
        if file_path == "EEROR":
            return("path time not found")
    STAT = os.stat(file_path)
    return time.strftime('%d-%m %H:%M', time.localtime(STAT[ST_MTIME]))

# =============================================================================
# def thresh_per_chanel(img, chan, MIN=0 ,MAX=255, win_name = "chanel"):
#     """try thresholding per RGB chanel"""
#     c = chan
#     c[np.where(chan<MIN)]=0
#     c[np.where(chan>=MAX)]=255
# #    if win_name != "chanel":
# #        cv2.namedWindow(win_name, cv2.WINDOW_NORMAL)
# #        cv2.imshow(win_name, c)
# #        cv2.waitKey(1)
#     return c
#
# def filter_for_10(frame):
#
#     b, g, r = cv2.split(frame)
#
#     vb = thresh_per_chanel(frame, b, 30 ,30, win_name = "blue")
#     vg = thresh_per_chanel(frame, g, 0 ,10, win_name = "green")
#     vr = thresh_per_chanel(frame, r, 0 ,10, win_name = "RED")
#
#     merge = cv2.merge((vb,vg,vr))
#
# #    cv2.namedWindow("nice", cv2.WINDOW_NORMAL)
# #    cv2.imshow("nice", merge)
#     return merge
#
# =============================================================================


