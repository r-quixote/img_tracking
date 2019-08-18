# -*- coding: utf-8 -*-
"""
Created on Sun Aug 18 16:25:05 2019

@author: YasmineMnb
"""

import os
import cv2
import numpy as np


def load_points_from_tracker_file(points_file):
    points_dct = {}
    with open (points_file, "r") as tracker_hist_data:
        for line in tracker_hist_data:
            dots = (line.split(", C")[0]).split(", ")
            dots = list(map(float, dots))
            x = (int(dots[0] + dots[2]/2))
            y = (int(dots[1] + dots[3]/2))
            file_name = line.split(",")[-2].split("\\")[-1]
            points_dct[file_name] = (x,y)
    return points_dct



def add_previous_points(points_dct, img,curr_pic_name ):
    points_lst = []
    for i in sorted(points_dct):
        points_lst.append(points_dct[i])
    print("pts_lst",points_lst)
    pts = np.array(points_lst, np.int32)
    print("pts", pts)
    cv2.polylines(img,[pts],False,(255,155,0))
    cv2.namedWindow('image', cv2.WINDOW_NORMAL)
    cv2.imshow('image', img)
    print("points_dct",points_dct)
    return img

def click_event(event, x, y, flags, param ):
    # what to do with which mous function -
    # param = (curr_pic, img, points)
    curr_pic_name = param[0]
    if event == cv2.EVENT_LBUTTONDOWN: ##left click:
        print(x,y)
        param[2][curr_pic_name] = (x,y)
        drawing_copy = param[1].copy()
        drawing_copy = cv2.circle(drawing_copy, (x, y), 1, (0, 255, 0), -1)
        cv2.imshow('image', drawing_copy)
        cv2.waitKey(1)

    elif event == cv2.EVENT_RBUTTONDOWN: ## right click:
        print("clean")
        param[2][curr_pic_name] = (-1,-1)
#        param[1] = cv2.imread(folder_path + "\\" + curr_pic_name)
        param[1] = param[3]
        cv2.imshow('image', param[1])
        cv2.waitKey(1)

def clickable_pic_loop(img, curr_pic, i, points):
    original_img = cv2.imread(folder_path + "\\" + curr_pic)
    img = cv2.imread(folder_path + "\\" + curr_pic)
#    if len(points)>1:
    img = add_previous_points(points, img, curr_pic)
    cv2.imshow('image', img)
    while True:
        cv2.setMouseCallback('image', click_event, param = [curr_pic, img, points, original_img])


        k=cv2.waitKey(1) & 0xFF
        if k==52: #4 key(numpad left)
            break
        elif k==54: #6 key(numpad right)
            break
        elif k==27: #Esc key(numpad right)
            break
        elif k==13: #Enter key (if used the trackbar)
            break
    i = cv2.getTrackbarPos("trackbar", "image")
    return k, i

def trackbar_func(val):
    #can't escape an empty func for createTrackbar
    pass


def loop_through_imgs(folder_path, points = {}, i = 0,
                      out_file=r"C:\Users\ronik\Desktop\123th_data.txt"):
    #list of imgs in the folder
    pic_lst = os.listdir(folder_path)
    #creat the window
    cv2.namedWindow('image', cv2.WINDOW_NORMAL)
    cv2.createTrackbar("trackbar", 'image' , 0, len(pic_lst), trackbar_func)
    #actual loop for the folder
    while i < len(pic_lst):
        curr_pic = pic_lst[i]
        img = cv2.imread(folder_path + "\\" + curr_pic)

        # update Trackbar and add points colected so far
        cv2.setTrackbarPos("trackbar", "image", i)

        # open curr_pic for clicking
        k,i = clickable_pic_loop(img,curr_pic, i, points)

        # how to continue:
        if k==27:
            print("you stoped the manual collection")
            break
        elif k==54: #6 key(numpad right) (NEXT)
            i += 1
        elif k==52: #4 key(numpad left) (BACK)
            i -= 1
        elif k==13: #Enter key (if used the trackbar)
            continue



    for i in points: print(i)
    print("you should save to this file now:", out_file)

out_file = r"C:\Users\ronik\Desktop\Xth_data.txt"
folder_path = r"C:\Users\YasmineMnb\Desktop\fluo playing\9\side_croped_3"

points_file = r"C:\Users\YasmineMnb\Desktop\fluo playing\9\9_croped_track_side_TEST\Rois_side_croped_3_YUV_Tip_3\CSRT.txt"
points_dct = load_points_from_tracker_file(points_file)

loop_through_imgs(folder_path, points_dct, 144)

#%%
