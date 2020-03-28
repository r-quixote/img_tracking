# -*- coding: utf-8 -*-
"""
Created on Thu Nov 15 13:26:09 2018

@author: Roni
"""
import cv2
import os
import time
import numpy as np
from stat import ST_MTIME
import traceback

import img_procesing
import progress_bar
from PIL import Image ## for gif

def get_orig_path(file_path):
    """
    used for get_time

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
    """
    still a bit shaky - ment to get the creation time from the output of lab
    nikon cams files - not for raspberry PI cams/webcams/other formats
    """
    if "CROPED" in file_path:
        file_path = get_orig_path(file_path)
        if file_path == "EEROR":
            return("path time not found")
    STAT = os.stat(file_path)
    try:
        creat_time = time.strftime('%d-%m %H:%M', time.localtime(STAT[ST_MTIME]))
    except:
        print("there was an error getting the creation time")
        return("path time not found")
    return creat_time

def create_video(input_folder_path, outvid_path, fps):
    """
    create video from images in input_folder_path
    fps needs to be a float type!
    """
    imgs_lst = os.listdir(input_folder_path)
# =============================================================================
#     ## get size from first img
#     ## there might be a limit to what your video player can show
#     ## so we half it (for now)
#     image0 = input_folder_path +"\\"+ imgs_lst[0]
#     img0 = cv2.imread(image0)
#     size = (int(img0.shape[1]/2), int(img0.shape[0]/2))
#     size = ((img0.shape[1]), (img0.shape[0]))
#     size = (640,480)
# =============================================================================
    size = (1280,720)

    ## set params for the vid_output
    is_color = True
    fourcc = cv2.VideoWriter_fourcc(*"XVID") ## .avi
#    fourcc = cv2.VideoWriter_fourcc(*'MP4V')  ## .mp4
    vid = cv2.VideoWriter(outvid_path, fourcc, fps, size, is_color)

    ## for the progress bar we need to note the start time
    t = time.perf_counter()
    job_len = len(imgs_lst) #for time estimate

    try:
#        frames = []            ## for gif saving
        for i in range(0, int(len(imgs_lst))):
            image_file = input_folder_path +"\\"+ imgs_lst[i]
            img = cv2.imread(image_file)
            if type(img) != np.ndarray: ## just trying to catch common errors
                break
# ========== if anything should be done with img enter code here ==============
#
#            img = img_procesing.rotate_img(img,180)
#
#            dots_img = remove_blue(img)
#            img = np.concatenate((img, dots_img), axis=1) ## add next to each other
#
#            size = (int(img.shape[1]/4), int(img.shape[0]/4))
#            size = (1500,1080)      ##(3145, 1016)
#            print(size[0], size[1])
#            print(size[0]/size[1])
#            break
            img = cv2.resize(img, size)
#            img_procesing.draw_on_img(img, img_procesing.get_time(image_file)) ## add time stamp
#
# =============================================================================

            ## show img while processing
            cv2.namedWindow("img", cv2.WINDOW_NORMAL)
            cv2.imshow("img", img)
            cv2.waitKey(1)

            ## write to video file
            vid.write(img)

            ## just for the progress bar:
            perc = i/len(imgs_lst)
            progress_bar.update_progress_bar(perc)

        progress_bar.update_progress_bar(1)

    except KeyboardInterrupt:
        print("cought: Keyboard Interrupt")

    vid.release()
    cv2.destroyAllWindows()

def create_gif(input_folder_path, output_path):

    imgs_lst = os.listdir(input_folder_path)
    frames = []
    for i in range(0,100):# int(len(imgs_lst))):
        image_file = input_folder_path +"\\"+ imgs_lst[i]

        img = cv2.imread(image_file)

        size = (640,480)
        img = cv2.resize(img, size)

        cv2.namedWindow("img", cv2.WINDOW_NORMAL)
        cv2.imshow("img", img)
        cv2.waitKey(1)

        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        im_pil = Image.fromarray(img)
        frames.append(im_pil)

        perc = i/len(imgs_lst)
        progress_bar.update_progress_bar(perc, "time")

    frames[0].save(output_path, format='GIF',
                      append_images=frames[1:500], save_all=True, duration=40, loop=0)

def main():
    input_folder_path = r"C:\Users\YasmineMnb\Desktop\pics_feb\1\side_croped_1"
    outvid_path = r"C:\Users\YasmineMnb\Desktop\pics_feb\1\side_croped_1.avi"
    create_video(input_folder_path, outvid_path, 24.0)
#    create_gif(input_folder_path,outvid_path.replace(".avi", ".gif"))

if __name__ == '__main__':
    main()