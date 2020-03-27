# -*- coding: utf-8 -*-
"""
Created on Sun Aug 18 16:37:26 2019

@author: roni
"""

import cv2
import numpy as np

# =============================================================================
#               basic clicking on blank img
# =============================================================================

def CallBackFunc(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print("Left button of the mouse is clicked - position ({}, {})".format(x,y))
        param[(x,y)] = "LEFT"
    elif event == cv2.EVENT_RBUTTONDOWN:
        print("Right button of the mouse is clicked - position ({}, {})".format(x,y))
    elif event == cv2.EVENT_MBUTTONDOWN:
        print("Middle button of the mouse is clicked - position  ({}, {})".format(x,y))


def main():
    # Create a black image and a window
    #%%
    lst = {}
    windowName = 'MouseCallback'
    img = np.zeros((800, 800, 3), np.uint8)
    cv2.namedWindow(windowName)
    # bind the callback function to window
    cv2.setMouseCallback(windowName, CallBackFunc, param = lst)
    while (True):
        cv2.imshow(windowName, img)
        if cv2.waitKey(20) == 27:
            break

    print(lst)
    cv2.destroyAllWindows()
#%%

if __name__ == "__main__":
    main()