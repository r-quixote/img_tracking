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
    crop the entire list of pictures -
    pic_list shoud be the list of the names of the files
    """
    #%
    t = time.perf_counter()
    def on_trackbar(val):
        pass

    cv2.namedWindow("croping", cv2.WINDOW_NORMAL)
    cv2.createTrackbar("track_bar", "croping" , 0, len(pic_lst), on_trackbar)

    for i in range(len(pic_lst)):
        pic_name = pic_lst[i]
        img = in_path + "\\" + pic_lst[i]

#        print(pic_name)
#        print(out_path)

        pic_name = out_path +"\\" + pic_name.split(".")[0].strip("DSC_")+"_CROPED.jpg"
#        print(pic_name)

        perc = (i/len(pic_lst))*100
#            print("%.2f" % perc, r"%")
        delt = time.perf_counter() - t
        if perc>0:
            estimate = (delt/perc)*100 - delt
            if estimate > 70:
                estimate = estimate/60
            estimate = "%.1f minutes"%(estimate)
            progress_bar.update_progress_bar(perc/100, "time left - "+ estimate)
#            update_progress(perc/100)
#            print("in {} seconds".format("%.2f" % delt))

        frame = cv2.imread(img)

        cv2.setTrackbarPos("track_bar", "croping", i)

        croped = crop(frame, x,y,h,w, "croping")

        rotated = img_procesing.rotate_img(croped)

        cv2.imshow("croping", rotated)
        cv2.waitKey(1)



        cv2.imwrite(pic_name,rotated)
    perc = (i/len(pic_lst))*100
    progress_bar.update_progress_bar(perc/100, " time left: "+str(estimate))
    print("\nin {} seconds".format(time.perf_counter() - t))
#%
def get_ROI(img):
    print("\nuse `space` or `enter` to finish selection")
    print("use `c`     or `Esc`   to cancel selection (function will return zero by zero)")
    cv2.namedWindow("SELECT ROI", cv2.WINDOW_NORMAL)
#    cv2.moveWindow("SELECT ROI",550,550)
    cv2.waitKey(1)
    bbox = cv2.selectROI("SELECT ROI", img, True)
    cv2.destroyWindow("SELECT ROI")
    return bbox

def creat_folder(out_path):
    # Create directory to save if not exist
    if os.path.isdir(out_path):
        ans = input("HEY! output folder already exists. \
		if u want to change it pleas enter new name now")
        if ans == "":
            print("OK then")
            return out_path
        n_path = out_path.rsplit('\\', 1)[0] + "\\" + ans
        creat_folder(n_path)
        return n_path
    if not os.path.isdir(out_path):
        os.mkdir(out_path)
        return out_path

 #%%
in_path = r"C:\Users\YasmineMnb\Desktop\New_folder_3"
out_path = r"C:\Users\YasmineMnb\Desktop\New_folder_4"

pic_lst  = os.listdir(in_path)
#pic_lst = pic_lst[:476]   ## for spesific stop...
if len(pic_lst) != len(os.listdir(in_path)): ##just for when i forget
    print("\n\nHEY!\n you didn't take all the pictures\n\n")

out_path = creat_folder(out_path)
## showing last pic of folder - click and drag to select region of interest (ROI)
last_pic_name_path = in_path + "\\" + pic_lst[-1]
last_img = cv2.imread(last_pic_name_path)


ROI = get_ROI(last_img)

#ROI = (683, 579, 3166, 2045)

cv2.destroyAllWindows()
#x = ROI[0]
#y = ROI[1]
#w = ROI[2]
#h = ROI[3]

if (ROI[2] or ROI[3]) == 0: ## if selection was canceled ROI has dimension of 0
    print("\n###############\
          you canceled...\
          ###############")

else:
    print("\nnow croping :)")
    crop_all(ROI[0], ROI[1], ROI[3], ROI[2], in_path, out_path, pic_lst)



#%%
# =============================================================================
#
#
# pic_lst  = os.listdir(r"C:\Users\YasmineMnb\Desktop\Roni_new\PERS\seeds\seed-reco\good")
# q = [int(i.replace(".JPG","")) for i in pic_lst]
# i = max(q)
# while True:
#
#     img = cv2.imread(r"C:\Users\YasmineMnb\Desktop\Roni_new\PERS\seeds\seed-reco\DSC_3162.JPG")
#     ROI = get_ROI(img)
#     if ROI[2:] == (0, 0):
#         print("\n\nstoped")
#         cv2.destroyAllWindows()
#         break
#     croped_im = crop(img, ROI[0], ROI[1], ROI[3], ROI[2], "croped")
#
#     pic_name  = r"C:\Users\YasmineMnb\Desktop\Roni_new\PERS\seeds\seed-reco\good\{}.JPG".format(i)
#
#     cv2.imwrite(pic_name,croped_im)
#     cv2.destroyAllWindows()
#     i +=1
#
#
#
# =============================================================================


