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
#%%
def rotate_img(img):
    import imutils
    rotated = imutils.rotate(img, 180)
#    cv2.imshow("Rotated", rotated)
#    cv2.waitKey(0)
    return rotated
#%%
# =============================================================================
#
#     in_path = r"C:\Users\YasmineMnb\Desktop\New folder (2)"
#     im = os.listdir(in_path)[0]
#     img = in_path + "\\" + im
#     img = cv2.imread(img)
#     rotate_img(img)
# =============================================================================



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
#%%    TRING TO ZOOM....

#def zoom_in(img, center_X,center_Y, scale):
#    height, width, channels = img.shape
#
#    radiusX,radiusY= int(scale*height/100),int(scale*width/100)
#
#    minX,maxX=centerX-radiusX,centerX+radiusX
#    minY,maxY=centerY-radiusY,centerY+radiusY
#
#    cropped = img[minX:maxX, minY:maxY]
#    resized_cropped = cv2.resize(cropped, (width, height))
#
#    cv2.imshow('my webcam', resized_cropped)
#
#
#
#
#def zoom_out(img):
#    pass
# =============================================================================
#
# def click_event(event, x, y, flags, param ):
#     # what to do with which mous function -
#     # param = [curr_pic, img, points, original_img]
#     curr_pic_name = param[0]
#     if event == cv2.EVENT_LBUTTONDOWN: ##left click:
#         print(x,y)
#         param[2][curr_pic_name] = ((x,y),"Manual")
#         drawing_copy = param[1].copy()
#         drawing_copy = cv2.circle(drawing_copy, (x, y), 1, (0, 255, 0), -1)
#         cv2.imshow("Tracking", drawing_copy)
#         cv2.waitKey(1)
#
#     elif event == cv2.EVENT_RBUTTONDOWN: ## right click:
#         print("clean")
#         param[2][curr_pic_name] = (-1,-1)
#         param[1] = param[3]
#         cv2.imshow("Tracking", param[1])
#         cv2.waitKey(1)
#
#     elif event == cv2.EVENT_MOUSEWHEEL:
#         if flags > 0:
#             print("zoom in")
#             zoom_in(img, (x,y))
#         else:
#             print("zoom out")
#
# def clickable_pic_loop(img, curr_pic, i, points_dct, folder_path, video_out):
#     original_img = cv2.imread(folder_path + "\\" + curr_pic)
#     img = cv2.imread(folder_path + "\\" + curr_pic)
# #    img = add_previous_points(points_dct, img, curr_pic)
#     cv2.imshow("Tracking", img)
#     while True:
#         cv2.setMouseCallback("Tracking", click_event, param = [curr_pic, img, points_dct, original_img])
#
#         k=cv2.waitKey(1) & 0xFF
#         if k==52: #4 key(numpad left)
#             break
#         elif k==54: #6 key(numpad right)
#             break
#         elif k==27: #Esc key(numpad right)
#             break
#         elif k==13: #Enter key (if used the trackbar)
#             break
#     i = cv2.getTrackbarPos("trackbar", "Tracking")
#
#     if video_out != None:
#         video_out.write(img)
#
#     return k, i
#
#
# folder_path =  r"C:\Users\YasmineMnb\Desktop\fluo playing\9\side_croped_3"
# curr_pic = os.listdir(folder_path)[0]
# video_out = None
# img = None
# i = 0
# points_dct= {}
# clickable_pic_loop(img, curr_pic, i, points_dct, folder_path, video_out)
#
# #%%
#
# import cv2
#
# def show_webcam(mirror=False):
#     scale=10
#
#
#     while True:
#
#
#         #get the webcam size
#         height, width, channels = img.shape
#
#         #prepare the crop
#         centerX,centerY=int(height/3),int(width/3)
#         radiusX,radiusY= int(scale*height/100),int(scale*width/100)
#
#         minX,maxX=centerX-radiusX,centerX+radiusX
#         minY,maxY=centerY-radiusY,centerY+radiusY
#
#         cropped = img[minX:maxX, minY:maxY]
#         resized_cropped = cv2.resize(cropped, (width, height))
#
#         cv2.imshow('my webcam', resized_cropped)
#         if cv2.waitKey(1) == 27:
#             break  # esc to quit
#
#         #add + or - 5 % to zoom
#         elif cv2.waitKey(1) == 52:
#             scale += 5  # +5
#             print("52")
#             print(scale)
#         elif cv2.waitKey(1) == 54:
#             scale -= 5  # +5
#             print("54")
#             print(scale)
#
# show_webcam(mirror=False)
# =============================================================================
