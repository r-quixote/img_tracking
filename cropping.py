"""
replace progress bar with tqdm!
"""

import time
import cv2
import os

import progress_bar
import img_procesing
from GUI import GUI

def multi_crop_img_lst(ROIs, out_paths, in_path):
    """
    crop all ROIs out of entire list of pictures in the in_path folder
    save them to the out_paths list
    """
    ## get a list of all the pics in the in_path folder
    pic_lst = [os.path.join(in_path, f_name) for f_name in os.listdir(in_path)]

    ## Track how long this takes
    t = time.perf_counter()

    for i, full_pic_path in enumerate(pic_lst):
        ## Create new file name for the croped img
        pic_name = full_pic_path.rsplit("\\", 1)[-1]
        new_pic_name = pic_name.strip(".JPG").strip("DSC_")+"_CROPED.jpg"

        ## Progress bar
        perc = (i/len(pic_lst))
        progress_bar.update_progress_bar(perc)

        ## Load img
        img = cv2.imread(full_pic_path)

        ## Loop over selected ROIs
        for j, ROI in enumerate(ROIs):
            ## Crope the img
            x, y, w, h = ROI[0], ROI[1], ROI[2], ROI[3]
            croped_img = img[y:y+h, x:x+w]

# ========= if anything should be done with imgs enter code here ==============
#            rtd = img_procesing.rotate_img(croped_img,180)
# =============================================================================

            ## create window for every ROI
            cv2.namedWindow("croping_" + str(ROI), cv2.WINDOW_NORMAL)
            cv2.imshow("croping_" + str(ROI), croped_img)

            ## Press Esc OR q key to stop
            k = cv2.waitKey(1) & 0xff
            if k == 27 or k == ord('q'):
                break

            ## Save the img to file
            out_path = out_paths[j] + "\\" + new_pic_name
            cv2.imwrite(out_path, croped_img)

        ## If we broke off we should stop this loop as well
        if k == 27 or k == ord('q'):
            print("\n\n!!! You Stoped !!!")
            break

    ## Progress bar to finish...
    if k != 27 and k != ord('q'):
        progress_bar.update_progress_bar(1)
        print("\n\nfinished in {}s ({} minutes)".format(round(time.perf_counter() - t),round((time.perf_counter() - t)/60,2)))



def creat_folder(out_path):
    """
    checks if the out_path exists
    if it exists it will ask if its ok to overwrite
    if not, it will create the directory
    """
    if os.path.isdir(out_path):
        ans = input("\nHEY!\n output folder already exists.\n \
                    to change it pleas enter new name now\n\n")
        if ans == "":
            print("OK then")
            return out_path
        else:
            n_path = out_path.rsplit('\\', 1)[0] + "\\" + ans
            creat_folder(n_path)
            return n_path
    else:
        os.mkdir(out_path)
        return out_path
#%% ROIs for R + L
""" R
[(4732, 1581, 490, 519),
(3728, 1625, 537, 450),
(3002, 1512, 693, 575),
(2201, 1600, 622, 493),
(1150, 1468, 645, 638)]

[(3912, 1843, 113, 107),
(3926, 1825, 70, 231),
(3195, 1675, 448, 368),
(2036, 1537, 674, 519),
(985, 1575, 579, 443)]

[(4663, 1497, 774, 706),
(3673, 1576, 581, 548),
(3068, 1564, 675, 591),
(2157, 1375, 826, 798),
(1050, 1308, 718, 762)]

[(4691, 1503, 680, 627),
(3635, 1455, 699, 657),
(3138, 1467, 600, 706),
(2172, 1345, 806, 883),
(877, 1321, 957, 852)]

[(4733, 1546, 600, 584),
(3710, 1436, 638, 676),
(3049, 1564, 567, 560),
(2125, 1424, 760, 670),
(1130, 1302, 783, 822)]

(4822, 1634, 450, 451)
(3790, 1658, 474, 421)
(3129, 1475, 525, 561)
(2312, 1469, 596, 646)
(1172, 1634, 629, 457)


"""

""" L
[(1027, 1771, 624, 530),
(2054, 1601, 812, 767),
(2950, 1625, 634, 658),
(3551, 1662, 680, 590),
(4451, 1528, 821, 779)]

[(947, 1783, 779, 518),
(1998, 1436, 812, 962),
(2828, 1668, 779, 578),
(3598, 1722, 591, 530)]

[(849, 1753, 792, 627),
(2096, 1753, 728, 536),
(2819, 1656, 732, 596),
(3565, 1674, 596, 578),
(4602, 1649, 623, 579)]

[(947, 1775, 707, 631),
(2106, 1806, 693, 569),
(2898, 1643, 613, 632),
(3553, 1587, 542, 669),
(4637, 1675, 542, 550)]

[(1017, 1762, 653, 622),
(2059, 1609, 755, 701),
(2814, 1609, 704, 641),
(3401, 1426, 741, 775),
(4390, 1426, 859, 781)]

[(1008, 1762, 638, 628),
(1815, 1585, 1098, 744),
(2805, 1567, 825, 664),
(3401, 1439, 825, 804),
(4437, 1567, 803, 640)]
"""
#(923, 1339, 4271, 989)

#%%
def main():
    ## Chosse folder to crop
#    in_path = GUI.filedialog_loop("choose input folder")
    in_path = r"C:\Users\YasmineMnb\Desktop\transfer folder\201123_contin_low\1_R\origin"
    pic_lst = [os.path.join(in_path, f_name) for f_name in os.listdir(in_path)]

    ## Showing last image of the in_path folder
    last_pic_name_path = pic_lst[-1]
    last_img = cv2.imread(last_pic_name_path)

    ## Add timestamp to last_img
    first_img_file_time = img_procesing.get_time(pic_lst[0])
    last_img_file_time = img_procesing.get_time(last_pic_name_path)
    text = "First frame time: {}\nLast frame time: {}".format(first_img_file_time, last_img_file_time)
    last_img_file_time = img_procesing.text_on_img(last_img, text)

    ## Select all ROIs (in roni exp from left to tright)
    ROIs = img_procesing.get_multiple_ROIs(last_img)

#    ROIs = [(1008, 1762, 638, 628),
#            (1815, 1585, 1098, 744),
#            (2805, 1567, 825, 664),
#            (3401, 1439, 825, 804),
#            (4437, 1567, 803, 640)]

    ## If there was nothing selected then don't try to crop
    if len(ROIs) == 0:
        print("\n\nyou canceled...\n")
    else:
        for roi in ROIs:
            print(roi)
        ## Creating folders for every ROI and save them to out_paths list
        parent_folder = in_path.rsplit("\\",1)[-2]
        out_paths = []
        for i in range(len(ROIs)):
            out_path = parent_folder + "\\Croped_" + str(i+1)
            out_path = creat_folder(out_path)
            out_paths.append(out_path)

        multi_crop_img_lst(ROIs, out_paths, in_path)

if __name__ == "__main__":
    try:
        main()
    finally:
        cv2.destroyAllWindows()