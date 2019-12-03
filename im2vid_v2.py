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
    nikon cams files - not for rasp pi cams
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

    ## get size from first img
    ## there might be a limit to what your video player can show
    ## so we half it (for now)
    image0 = input_folder_path +"\\"+ imgs_lst[0]
    img0 = cv2.imread(image0)
#    size = ((img0.shape[1]), (img0.shape[0]))
    size = (int(img0.shape[1]/2), int(img0.shape[0]/2))

    ## set params for the vid_output
    is_color = True
    fourcc = cv2.VideoWriter_fourcc(*"XVID") ## .avi
#    fourcc = cv2.VideoWriter_fourcc(*'MP4V')  ## .mp4
    vid = cv2.VideoWriter(outvid_path, fourcc, fps, size, is_color)

    ## progress tracking..
    t = time.perf_counter()

    ## actual loop:
    try:
#        frames = []            ## for gif saving
        for i in range(0, int(len(imgs_lst))):
            image_file = input_folder_path +"\\"+ imgs_lst[i]
            img = cv2.imread(image_file,1)
            if type(img) != np.ndarray: ## just trying to catch common errors
                break
# ========== if anything should be done with img enter code here ==============
#            img = img_procesing.rotate_img(img,180)
#
#            dots_img = remove_blue(img)
#            img = np.concatenate((img, dots_img), axis=1) ## add next to each other
#            size = (int(img.shape[1]/4), int(img.shape[0]/4))
#            size = (1500,1080)      ##(3145, 1016)
#            print(size[0], size[1])
#            print(size[0]/size[1])
#            break
#            img = cv2.resize(img, size)
#
#            img_procesing.draw_on_img(img, img_procesing.get_time(image_file)) ## add time stamp
#
#            #save as gif
#            if i%4 ==0:
#                img4 = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#                im_pil = Image.fromarray(img4)
#                frames.append(im_pil)
# =============================================================================

            ## show img while processing
            cv2.namedWindow("img", cv2.WINDOW_NORMAL)
            cv2.imshow("img", img)
            cv2.waitKey(1)

            vid.write(img)

            ## just for progress tracking:
            perc = i/len(imgs_lst)
            if perc >0:
                delt = time.perf_counter() - t
                estimate = (delt/perc) - delt
                estimate = int(estimate)
                if estimate > 70:
                    estimate = str(int(estimate/60))+" min"
                else: estimate = str(estimate) + " sec"
                progress_bar.update_progress_bar(perc, " time left ~ " + estimate)
        progress_bar.update_progress_bar(1, "\nDone")

    except KeyboardInterrupt:
        print("cought: Keyboard Interrupt")

# ==== for gif saving =========================================================
#
#    frames[0].save(r'C:\Users\YasmineMnb\Desktop\2_test.gif', format='GIF',
#                  append_images=frames[1:], save_all=True, duration=100, loop=0)
#
# =============================================================================
    vid.release()
    cv2.destroyAllWindows()

def create_gif(input_folder_path, output_path):
    from PIL import Image

    imgs_lst = os.listdir(input_folder_path)
    frames = []
    for i in range(0, int(len(imgs_lst))):
        image_file = input_folder_path +"\\"+ imgs_lst[i]
        pil_im = Image.open(image_file)
        frames.append(pil_im)

        perc = i/len(imgs_lst)
        progress_bar.update_progress_bar(perc, "time")

    frames[0].save(output_path, format='GIF',
                      append_images=frames[:500], save_all=True, duration=10, loop=0)

def main():
    input_folder_path = r"C:\Users\YasmineMnb\Desktop\agueda and cini\100D7500_croped_4"
    outvid_path = r"C:\Users\YasmineMnb\Desktop\agueda and cini\100D7500_croped_4.avi"
    create_video(input_folder_path, outvid_path, 12.0)


if __name__ == '__main__':
    main()