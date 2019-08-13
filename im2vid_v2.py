# -*- coding: utf-8 -*-
"""
Created on Thu Nov 15 13:26:09 2018

@author: Roni
"""
import cv2
import os
import progress_bar
import time
import numpy as np
from stat import ST_MTIME
import traceback
#%%
# ============================================================================= 

# ==================================2DO!!!=====================================
#                                   
# import re
# txt = "The rain in Spain"
# x = re.search("^The.*Spain$", txt)
# 
#                                   
# ==================================2DO!!!====================================
def get_orig_time(file_path):
    """
    will only work if both in same directroy:
    "...\8\side_croped" AND "...\8\side"
    """
    try:
        base_folder = file_path.split("_croped")[0]
        cur_file_name = file_path.rsplit("\\",1)[1]
        file_numb = cur_file_name.replace("_CROPED", "")
        
# ==================================2DO!!!=====================================
        full_or_file_path = base_folder + "\\DSC_"+ file_numb
# ==================================2DO!!!=====================================
        
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
        file_path = get_orig_time(file_path)
        if file_path == "EEROR":
            return("path time not found")
    STAT = os.stat(file_path)
    return time.strftime('%d-%m %H:%M', time.localtime(STAT[ST_MTIME]))

def draw_on_img(img, text):
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_size = img.shape[0]/400
    if font_size>6: font_size = 6
    img_with_text = cv2.putText(img, text, (10,int(img.shape[0]/6)), font, font_size,(255,255,255),2,cv2.LINE_AA)
    return img_with_text

def remove_blue(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    lower_red = np.array([135,0,0])
    upper_red = np.array([255,255,255])
    red_mask = cv2.inRange(hsv, lower_red, upper_red)
    
    lower_yellow = np.array([65,0,0])
    upper_yellow = np.array([88,255,255])
    yellow_mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
    
    full_mask = yellow_mask | red_mask
    
    res = cv2.bitwise_or(img,img, mask= full_mask)
    return res 


# =============================================================================
def create_video(input_folder_path, outvid_path, fps):
    """
    create video from images in input_folder_path
    FPS NEEDS TO BE FLOAT!
    """
    imgs_lst = os.listdir(input_folder_path)
    
    #get size from first img, there might be limit to this, so half it (for now)
    image0 = input_folder_path +"\\"+ imgs_lst[0]
    img0 = cv2.imread(image0)
    
    size = (img0.shape[1], img0.shape[0])
#    size = (int(img0.shape[1]/2), int(img0.shape[0]/2))
    
    #set params for the vid_output
    is_color = True
    fourcc = cv2.VideoWriter_fourcc(*"XVID")
    vid = cv2.VideoWriter(outvid_path, fourcc, fps, size, is_color)
    
    t = time.perf_counter()
    try:
        for i in range(0, int(len(imgs_lst))):
            
            image_file = input_folder_path +"\\"+ imgs_lst[i]
            img = cv2.imread(image_file,1)
            if type(img) != np.ndarray:
                break
            img = cv2.resize(img, size)
            
    # ====if anything should be done with img enter code here======================
             
            draw_on_img(img, get_time(image_file))
    #        img = remove_blue(img)
             
    # =============================================================================
    
            #show img while processing
            cv2.namedWindow("img", cv2.WINDOW_NORMAL) 
            cv2.imshow("img", img)
            cv2.waitKey(1)
            
            vid.write(img)
            
            ##just for progress tracking:
            
            perc = i/len(imgs_lst)
            if perc >0:
                delt = time.perf_counter() - t
                estimate = (delt/perc) - delt
                estimate = int(estimate)
                if estimate > 70:
                    estimate = str(int(estimate/60))+" min"
                else: estimate = str(estimate) + " sec"
                progress_bar.update_progress_bar(perc, " time left ~ " + estimate)
            
    #        if percentge % 1 == 0:
    #            if curr_perc!= percentge:
    #                curr_perc = percentge
    #                print(str(percentge) + "%")
        progress_bar.update_progress_bar(1, "\nDone")   
    except KeyboardInterrupt as e:
        print("cought:", e) 
    vid.release()

input_folder_path = r"C:\Users\YasmineMnb\Desktop\fluo playing\7 top only\top_croped_3"
outvid_path = r"C:\Users\YasmineMnb\Desktop\7_test_02.avi"

create_video(input_folder_path, outvid_path, 24.0) 

    
#%% Vid2Im

# =============================================================================
# 
# vidcap = cv2.VideoCapture(r"C:\Users\YasmineMnb\Desktop\for show\lab meeting\s3.mp4")
# success,image = vidcap.read()
# cnt = 0
# while success:
#     if len(str(cnt)) == 1:
#         name = "000"+ str(cnt)
#     elif(len(str(cnt))) == 2:
#         name = "00" + str(cnt)
#     elif(len(str(cnt))) == 3:
#         name = "0" + str(cnt)
#     elif(len(str(cnt))) == 4:
#         name = str(cnt)
#     print(name)
#     #  print('Read a new frame: ', success)
#     cnt += 1
#     success,image = vidcap.read()
#     
#     
#     cv2.imwrite(r"C:\Users\YasmineMnb\Desktop\test2\frame%s.jpg" % name, image)     # save frame as JPEG file      
# 
# 
#   
#   
# =============================================================================
