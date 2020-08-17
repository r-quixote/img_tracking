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
#    cv2.moveWindow("SELECT ROI",550,550) # usfull in case it opens in a bad location
    cv2.waitKey(1)
    bbox = cv2.selectROI("SELECT ROI", img, True)
    cv2.destroyWindow("SELECT ROI")
    return bbox

def get_multiple_ROIs(frame):
    """allows choosing multiple 'Regeions Of Interest' and returns them as list"""

    ## Creat a copy of the frame to show selected boxes
    show_selected_frame = frame.copy()

    ## init an empty list for the ROIs
    bboxs = []
    while True:
        cv2.namedWindow("SELECT ROI", cv2.WINDOW_NORMAL)
        bbox = cv2.selectROI("SELECT ROI", show_selected_frame, showCrosshair=True)
        if bbox == (0, 0, 0, 0):
            break
        bboxs.append(bbox)
        # drawing the selected boxes on the copy:
        for bbox in bboxs:
            show_selected_frame = cv2.rectangle(show_selected_frame, (bbox[0], bbox[1]), (bbox[0]+bbox[2],bbox[1]+ bbox[3]),
                                                (50, 50, 200) , 4)
            show_selected_frame = cv2.line(show_selected_frame, (bbox[0]+int(bbox[2]/2), bbox[1]), (bbox[0]+int(bbox[2]/2), bbox[1]+ bbox[3]),(50, 50, 200),2)
            show_selected_frame = cv2.line(show_selected_frame, (bbox[0], bbox[1]+int(bbox[3]/2)), (bbox[0]+bbox[2], bbox[1]+int(bbox[3]/2)),(50, 50, 200),2)

    cv2.destroyWindow("SELECT ROI")
    return bboxs

def crop(img, x, y, h, w, name):
    """
    shows the croped version of img, and returns it
    img - the image that you want to crop
    x,y - starting coordinate
    h,w - hight and width
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
    p.imshow(img[:,:,2], vmin = 0, vmax = 255) ##use this to find the color range!

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
        base_folder = file_path.rsplit("\\",2)[0]
        cur_file_name = file_path.rsplit("\\",1)[1]
        file_numb = cur_file_name.split("_")[0]
        full_or_file_path = base_folder + "\\origin\\DSC_"+ file_numb + ".jpg"

    except IndexError as err:
        traceback.print_tb(err.__traceback__)
        print(err)
        print("check the names of the folders")
        return "ERROR"
    except FileNotFoundError as err:
        traceback.print_tb(err.__traceback__)
        print(err)
        print("check the names of the folders")
        return "ERROR"
    return full_or_file_path

def get_time(file_path):
    if "CROPED" in file_path:
        file_path = get_orig_path(file_path)
        if file_path == "ERROR":
            return("path time not found")

    if not os.path.isfile(file_path):
        return("path time not found")
    STAT = os.stat(file_path)
    return time.strftime('%d-%m %H:%M', time.localtime(STAT[ST_MTIME]))

def get_time_delta(str_img_time, cur_img_time):
    """converts both to time_since_epoch and the converts back to string in 00:00 H form"""
    # convert start
    if str_img_time == "path time not found":
        return "time_error"
    start_time = time.strptime(str_img_time+" -2000", '%d-%m %H:%M -%Y') # year added cause default dosn't work
    epoch_start = time.mktime(start_time)

    # convert curr_img
    curr_time = time.strptime(cur_img_time+" -2000", '%d-%m %H:%M -%Y') # year added cause default dosn't work
    epoch_curr = time.mktime(curr_time)

    # get delta and convert back to string
    delta = epoch_curr - epoch_start


    H = str(int(delta/60/60))
    M = int(delta/60 % 60)
    if M<10:
        M = "0" + str(M)
    else:
        M = str(M)
    delt_str = H+":"+M
#    else:
#        delt_str = time.strftime('%H:%M',time.localtime(delta))
    return delt_str



def text_on_img(img, text, dx=0, dy=0):
    font = 5
    font_size = img.shape[0]/1000
    if img.shape[1]*1.5 < img.shape[0]:
        font_size = img.shape[1]/500
        font_thickness = 2
    font_thickness = 3
    if font_size>6:
        font_size = 6
    if font_size<1:
        font_size = 1
        font_thickness = 1
    init_x_pos = int(img.shape[1]/8)
    init_y_pos = int(img.shape[0]/6)
    # in case of multi line:
    text = text.split("\n")
    text_hight = cv2.getTextSize(text[0], font, font_size, font_thickness)[0][1]
    y_gap = int(text_hight*1.5)
    for i,line in enumerate(text):
        pos = (init_x_pos, init_y_pos+y_gap*i)
        img_with_text = cv2.putText(img, line, pos, font, font_size,(90,255,30),font_thickness)
    return img_with_text

def rotate_img(img, angle):
    import imutils
    rotated = imutils.rotate(img, angle)
#    cv2.imshow("Rotated", rotated)
#    cv2.waitKey(0)
    return rotated

def resize_img(img, scale_percent):

    if scale_percent > 1:
        width = int(img.shape[1] * scale_percent / 100)
        height = int(img.shape[0] * scale_percent / 100)
    else:
        width = int(img.shape[1] * scale_percent)
        height = int(img.shape[0] * scale_percent)
    dim = (width, height)
    # resize image
    resized = cv2.resize(img, dim)
    return resized

def copy_folder_content(in_path, out_path):
    import shutil
    pic_lst  = os.listdir(in_path)
    for i in range(len(pic_lst)):
        if len(pic_lst[i])>8:
            new_name = pic_lst[i].replace("0","",1)
        else:
            new_name = pic_lst[i]
        src = in_path + "\\" +  pic_lst[i]
        dst = out_path + "\\" +  new_name
#        print(src,"\n", dst)
        shutil.copy(src,dst)

def rename_folder_content(folder_path, start_num, out_path = None, name_format = "DSC_"):
    padding_num = 4
    ## get list of file names in the folder
    pic_lst  = os.listdir(folder_path)
    ## loop through said list
    cnt = start_num
    for i in range(len(pic_lst)):
        zero_padded_num = str(cnt).zfill(padding_num)
        new_f_name = name_format  + zero_padded_num + "." + pic_lst[i].split(".")[-1]

        ## if out_path was specified - move the file there with the new name
        if not out_path:
            out_path = folder_path

        new_path = out_path + "\\" + new_f_name
        origin_path = folder_path + "\\" + pic_lst[i]
#            print(origin_path+"\n"+new_path)
        try:
            os.rename(origin_path, new_path)
        except FileExistsError:
            if cnt == start_num:
                print("File Exists Error\nsaving with extra zero padding")
            padding_num = 5
            zero_padded_num = str(cnt).zfill(5)
            new_f_name = name_format + zero_padded_num + "." + pic_lst[i].split(".")[-1]
            new_path = folder_path + "\\" + new_f_name
            os.rename(origin_path, new_path)
        cnt += 1
