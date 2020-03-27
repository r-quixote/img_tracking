import time
import cv2
import os
import progress_bar
import img_procesing

def crop(img, x, y, h, w, name):
    """
    shows the croped version of img, and returns it
    img - the image that you want to crop
    name - the window name
    """
    crop_img = img[y:y+h, x:x+w]
#    cv2.namedWindow(name, cv2.WINDOW_NORMAL)
#    cv2.imshow(name, crop_img)
#    cv2.waitKey(1)
    return crop_img

def crop_all(x,y,h,w, in_path, out_path, pic_lst):
    """
    crop the entire list of pictures
    pic_list shoud be a list of the names of the files
    """
    ## need this for the progress bar
    t = time.perf_counter()
    cv2.namedWindow("croping", cv2.WINDOW_NORMAL)

    for i in range(len(pic_lst)):
        pic_name = pic_lst[i]
        img = in_path + "\\" + pic_lst[i]
        new_pic_name = out_path +"\\" + pic_name.split(".")[0].strip("DSC_")+"_CROPED.jpg"

        ##progress bar
        perc = (i/len(pic_lst))*100
        delt = time.perf_counter() - t
        if perc>0:
            estimate = (delt/perc)*100 - delt
            if estimate > 70:
                estimate = estimate/60
            estimate = "%.1f minutes"%(estimate)
            progress_bar.update_progress_bar(perc/100, "time left - "+ estimate)

        ## actual croping
        frame = cv2.imread(img)
        croped = crop(frame, x,y,h,w, "croping")

# ========= if anything should be done with imgs enter code here ===============
#         rtd = img_procesing.rotate_img(croped,180) ## for instance rotation
# =============================================================================

        cv2.imshow("croping", croped)
        cv2.waitKey(1)
        cv2.imwrite(new_pic_name,croped)

    ##progress bar again...
    perc = (i/len(pic_lst))*100
    progress_bar.update_progress_bar(perc/100, " time left: "+str(estimate))
    print("\nin {} seconds".format(time.perf_counter() - t))

def get_ROI(img):
    """
    returns the bounding box of selected area.
    x = bbox[0]
    y = bbox[1]
    w = bbox[2]
    h = bbox[3]
    use `space` or `enter` to confirm selection
    use   `c`   or  `Esc`  to cancel selection (function will return zero by zero)
    """
    cv2.namedWindow("SELECT ROI", cv2.WINDOW_NORMAL)
    cv2.waitKey(1)
    print("\nuse `space` or `enter` to confirm selection")
    print("use `c`     or `Esc`   to cancel selection (function will return [0,0])\n")
    bbox = cv2.selectROI("SELECT ROI", img, True)
    cv2.destroyWindow("SELECT ROI")
    return bbox

def creat_folder(out_path):
    """
    checks if the out_path exists,
    if exists: it will ask if its ok to overwrite
    if not:    it will create the directory
    """
    if os.path.isdir(out_path):
        ans = input("HEY! output folder already exists. \
                    ant to change it pleas enter new name now")
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
    in_path = r"C:\Users\YasmineMnb\Desktop\pics_feb\1\side_croped_2"
    out_path = r"C:\Users\YasmineMnb\Desktop\pics_feb\1\test"

    pic_lst  = os.listdir(in_path)
    #pic_lst = pic_lst[:476]   ## for spesific stop...
    ## in case i forget to turn back to all pics:

    if len(pic_lst) != len(os.listdir(in_path)):
        print("\n\nHEY!\n you didn't take all the pictures\n\n")

    out_path = creat_folder(out_path)

    ## showing last pic of folder
    last_pic_name_path = in_path + "\\" + pic_lst[-1]
    last_img = cv2.imread(last_pic_name_path)
    ## add timestamp to img
    first_img_file_time = img_procesing.get_time(in_path + "\\" + pic_lst[0])
    last_img_file_time = img_procesing.get_time(last_pic_name_path)
    text = "First frame time: {}\nLast frame time: {}".format(first_img_file_time,
                                                              last_img_file_time)
    last_img_file_time = img_procesing.text_on_img(last_img, text)

    ## click and drag to select region of interest (ROI)
    ROI = get_ROI(last_img)
    cv2.destroyAllWindows()

    ## if selection was canceled (ESC) ROI has dimension of 0
    if (ROI[2] or ROI[3]) == 0:
        print("\n###############\
              you canceled...\
              ###############")
    else:
        print("\nnow croping :)")
        crop_all(ROI[0], ROI[1], ROI[3], ROI[2], in_path, out_path, pic_lst)

if __name__ == "__main__":
    main()