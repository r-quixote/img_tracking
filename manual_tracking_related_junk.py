# -*- coding: utf-8 -*-
"""
Created on Sun Aug 18 09:36:59 2019

@author: YasmineMnb
"""

import cv2
import os
import numpy as np

in_path = r"C:\Users\YasmineMnb\Desktop\fluo playing\9\9_side"
pic_lst  = os.listdir(in_path)

last_pic_name_path = in_path + "\\" + pic_lst[-1]
last_img = cv2.imread(last_pic_name_path)



def trackbar_func(val):
    img_path = in_path + "\\" + pic_lst[val]
    img = cv2.imread(img_path)
    cv2.imshow(title_window, img)





title_window = "with BAR"

trackbar_name = "track bar"

cv2.namedWindow(title_window, cv2.WINDOW_NORMAL)
cv2.createTrackbar(trackbar_name, title_window , 0, len(pic_lst), trackbar_func)

cv2.waitKey(1)

#%%
cv2.setTrackbarPos("bar_name", "window_name", iteraion_num) ## to be added inside the loop


#%%


k = cv2.waitKey(1)
if k == 27:         # wait for ESC key to exit
    cv2.destroyAllWindows()
elif k == ord('s'): # wait for 's' key to save and exit
    print(i)


    #%%





import cv2
import numpy as np

drawing = False # true if mouse is pressed
mode = True # if True, draw rectangle. Press 'm' to toggle to curve
ix,iy = -1,-1

# mouse callback function
def draw_circle(event,x,y,flags,param):
    global ix,iy,drawing,mode

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix,iy = x,y

    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing == True:
            if mode == True:
                cv2.rectangle(img,(ix,iy),(x,y),(0,255,0),-1)
            else:
                cv2.circle(img,(x,y),5,(0,0,255),-1)

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        if mode == True:
            cv2.rectangle(img,(ix,iy),(x,y),(0,255,0),-1)
        else:
            cv2.circle(img,(x,y),5,(0,0,255),-1)



img = np.zeros((512,512,3), np.uint8)
cv2.namedWindow('image')
cv2.setMouseCallback('image',draw_circle)

while(1):
    cv2.imshow('image',img)
    k = cv2.waitKey(1) & 0xFF
    if k == ord('m'):
        mode = not mode
    elif k == 27:
        break

cv2.destroyAllWindows()




#%%     OLD VERSION - BACKUPP!!!!



import os
import cv2
import numpy as np


out_file = r"C:\Users\ronik\Desktop\Xth_data.csv"

folder_path = r"C:\Users\YasmineMnb\Desktop\plant_psycho\5\croped_1"

pic_lst = os.listdir(folder_path)

def open_pic(pic_name):
    img = cv2.imread(folder_path + "\\" + pic_name)
    cv2.namedWindow(pic_name, cv2.WINDOW_NORMAL)
    cv2.imshow(pic_name,img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return img

###                         OLD VERSION - BACKUPP!!!!
#img = open_pic(pic_lst[5])

def click_event(event, x, y, flags, param):
    global img
    global pic
    if event == cv2.EVENT_LBUTTONDOWN:
        print(x,y)
        points.append((x,y))
        cv2.circle(img, (x, y), 5, (0, 0, 255), -1)
#        cv2.imshow('image', img)
        pts = np.array(points, np.int32)
        cv2.polylines(img,[pts],False,(255,255,0)) ## for adding hist track
    elif event == cv2.EVENT_RBUTTONDBLCLK:
        print("cleaned")
        del points[-1]
        img = cv2.imread(folder_path + "\\" + pic)
        cv2.imshow('image', img)

###                         OLD VERSION - BACKUPP!!!!
points = []
global pic
for pic in pic_lst:

    global img
    img = cv2.imread(folder_path + "\\" + pic)

    while(1):
        cv2.setMouseCallback('image', click_event)
        cv2.imshow('image', img)
        k=cv2.waitKey(1) & 0xFF
###                         OLD VERSION - BACKUPP!!!!
        if k==27: #Escape KEY
            break
        cv2.imshow('image', img)

    cv2.destroyAllWindows()

#%%

import os
import cv2
import numpy as np


def add_previous_points(point_dct):
    global img
    points_lst = []
    for i in point_dct.values():
        points_lst.append(i[0])
    pts = np.array(points_lst, np.int32)
    cv2.polylines(img,[pts],False,(255,155,0), 1, 4)
    cv2.namedWindow('image', cv2.WINDOW_NORMAL)
    cv2.imshow('image', img)
    return img

def click_event(event, x, y, flags, param ):
    # what to do with which mous function -
    global img
    curr_pic_name = param[0]
    i = param[1]
    if event == cv2.EVENT_LBUTTONDOWN: ##left click:
        print(x,y)
        points[curr_pic_name] = ((x,y),"i = " + str(i))
        cv2.circle(img, (x, y), 1, (0, 255, 0), -1)

    elif event == cv2.EVENT_RBUTTONDBLCLK: ## right click:
        print("clean")
#        del points[-1]
#        points[params[1]] = (-1,-1)
        img = cv2.imread(folder_path + "\\" + curr_pic_name)
        cv2.imshow('image', img)
        cv2.waitKey(1)

def clickable_pic_loop(curr_pic, i):
    global img
    while True:
        cv2.setMouseCallback('image', click_event, param = (curr_pic, i))
        cv2.imshow('image', img)

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


out_file = r"C:\Users\ronik\Desktop\Xth_data.txt"
folder_path = r"C:\Users\YasmineMnb\Desktop\fluo playing\9\side_croped_3"





def loop_through_imgs(folder_path, points = {}, i = 0,
                      out_file=r"C:\Users\ronik\Desktop\%sth_data.txt"
                      %folder_path.split("\\")[-1]):
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
#        add_previous_points(points)

        # open curr_pic for clicking
        k,i = clickable_pic_loop(curr_pic, i)

        # how to continue:
        if k==27:
            print("you stoped - completely...")
            break
        elif k==54: #6 key(numpad right) (NEXT)
            i += 1
        elif k==52: #4 key(numpad left) (BACK)
            i -= 1
        elif k==13: #Enter key (if used the trackbar)
            continue

loop_through_imgs(folder_path)



#%%
import cv2
img = cv2.imread(folder_path + "\\" + curr_pic) # load a dummy image
while(1):
    cv2.imshow('img',img)
    k = cv2.waitKey(33)
    if k==27:    # Esc key to stop
        break
    elif k==-1:  # normally -1 returned,so don't print it
        continue
    else:
        print(k) # else print its value













