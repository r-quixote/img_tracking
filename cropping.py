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

    ## Progress bar to finih...
    if k != 27 and k != ord('q'):
        progress_bar.update_progress_bar(1)
        print("\n\nfinished in {} seconds".format(round(time.perf_counter() - t,2)))


def creat_folder(out_path):
    """
    checks if the out_path exists,
    if exists: it will ask if its ok to overwrite
    if not:    it will create the directory
    """
    if os.path.isdir(out_path):
        ans = input("\nHEY!\n output folder already exists.\n \
                    to change it pleas enter new name now\n\n")
        if ans == "":
            print("OK then")
            return out_path
        n_path = out_path.rsplit('\\', 1)[0] + "\\" + ans
        creat_folder(n_path)
        return n_path
    if not os.path.isdir(out_path):
        os.mkdir(out_path)
        return out_path


def main():
    ## Chosse folder to crop
#    in_path = GUI.filedialog_loop("choose input folder")
    in_path = r"C:\Users\YasmineMnb\Desktop\june exp\200623_contin\2\origin"
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

    ## If there was nothing selected then don't try to crop
    if len(ROIs) == 0:
        print("\n\nyou canceled...\n")

    else:
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