import cv2
import sys
import os.path
import re
import progress_bar
import img_procesing
import manual_tracking


# Save tracked objects rois
def save_result_rois(output_folder, boxes, bbox_inits, tracker_types, init,
                       object_name, file_name,
                     output_path, first_tiral):
    # Create directory to save
    pic_time = img_procesing.get_time(file_name)
    dirName = os.path.dirname(output_folder)
    videoName = os.path.splitext(os.path.basename(output_folder))
    dirName = dirName + "\\" + output_path
    if not os.path.isdir(dirName):
        os.mkdir(dirName)
    dirName = dirName + "\\Rois_" + videoName[0] + "_" + object_name
    if not os.path.isdir(dirName):
        os.mkdir(dirName)

    # Create files and save init box as first line
    if init:
        # Save trackers init roi
        for i in range(len(tracker_types)):
            # roi file path
            path_tracker_rois = dirName + "\\" + tracker_types[i] + '.txt'
            # create tracker file
            if first_tiral:
                my_file = open(path_tracker_rois, 'w+')
            else:
                my_file = open(path_tracker_rois, 'a')

            for j, bbox_init in enumerate(bbox_inits):
                print("i = {}, j = {}, bbox = {}".format(i,j,bbox_init))
                my_file.writelines(", ".join([str(s) for s in list(bbox_init)])+
                                   ", " + file_name + ", "+ pic_time + ", "
                                   + str(j) + ", Start \n")
            # close file
            my_file.close()
        return path_tracker_rois
    else: # (if not init)
        # Append files and save current box
        for i in range(len(tracker_types)):
            for j, new_box in enumerate(boxes):
                # roi file path
                path_tracker_rois = dirName + "\\" + tracker_types[i] + '.txt'
                with open(path_tracker_rois, "a") as my_file:
                    my_file.writelines(", ".join([str(round(s, 2)) for s in list(new_box)]) + ", " +
                                       file_name +", "+ pic_time + ", " + str(j) + ", Auto\n")
        return path_tracker_rois


# set video output for saving
def create_video_results(video_or_folder_name, frame,   object_name, output_path):
    dirName = os.path.dirname(video_or_folder_name)
    videoName = os.path.splitext(os.path.basename(video_or_folder_name))
    dirName = dirName + "\\" + output_path
    if not os.path.isdir(dirName):
        os.mkdir(dirName)
    save_video_name = dirName + "\\" + videoName[0] + object_name + ".avi"
    fourcc = cv2.VideoWriter_fourcc(*"XVID")
    frame_height, frame_width, layers = frame.shape
    video_out = cv2.VideoWriter(save_video_name, fourcc, 24.0, (frame_width, frame_height))
    print("video will be saved to: " + save_video_name)
    return video_out

# create list of colors to use to show trackers
def get_box_colors():
    colors = []
    colors.append((0, 0, 0))  # Black
    colors.append((255, 0, 0))  # Red
    colors.append((0, 255, 0))  # Lime
    colors.append((0, 0, 255))  # Blue
    colors.append((255, 255, 0))  # Yellow
    colors.append((0, 255, 255))  # Cyan
    colors.append((255, 0, 255))  # Magenta
    colors.append((192, 192, 192))  # Silver
    colors.append((128, 128, 128))  # Gray
    colors.append((128, 0, 0))  # Maroon
    colors.append((128, 128, 0))  # Olive
    colors.append((0, 128, 0))  # Green
    colors.append((128, 0, 128))  # Purple
    colors.append((0, 128, 128))  # Teal
    colors.append((0, 0, 128))  # Navy
    colors.append((188, 143, 143))  # rosy brown
    colors.append((230, 230, 250))  # lavender
    colors.append((244, 164, 96))  # sandy brown
    colors.append((0, 206, 209))  # dark turquoise
    colors.append((64, 224, 208))  # turquoise
    colors.append((72, 209, 204))  # turquoise pale
    colors.append((175, 238, 238))  # turquoise aqua
    colors.append((127, 255, 212))  # aqua marine
    colors.append((255, 0, 255))  # magenta / fuchsia
    colors.append((218, 112, 214))  # orchid
    colors.append((199, 21, 133))  # medium violet
    colors.append((219, 112, 147))  # pale violet
    colors.append((255, 20, 147))  # deep pink
    colors.append((255, 105, 180))  # hot pink
    return colors


# Return a list of all file names in path which are images
def list_images_in_path(directory):
    included_extensions = ['jpg', 'bmp', 'png', 'gif', 'jpeg', 'JPG', 'JPEG']
    onlyfiles = [f for f in os.listdir(directory)
                 if any(f.endswith(ext) for ext in included_extensions)]

    onlyfiles.sort(key=lambda var: [int(x) if x.isdigit() else x for x in re.findall(r'[^0-9]|[0-9]+', var)])
    full_path_files = [directory + '\\' + s for s in onlyfiles]

    return full_path_files


# Draw the detected bounding box, fps and tracker name on a given frame
def draw_bounding_box(frame, boxes, tracker_ok, timer, #ground_truth_bbox,
                      tracker_types, colors, i_frame, path_tracker_rois):
    # Calculate Frames per second (FPS)
#    fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)

    color_i = 0

    # draw tracked objects
    for i, new_box in enumerate(boxes):
        color_i = color_i + 1

        p1 = (int(new_box[0]), int(new_box[1]))
        p2 = (int(new_box[0] + new_box[2]), int(new_box[1] + new_box[3]))
#        tracker_type = tracker_types[i]

        cv2.rectangle(frame, p1, p2, colors[i + 1], 2, 4)
# =============================================================================
#         # show rectangle in another page
#         crop_img = frame[int(new_box[1]):int(new_box[1])+int(new_box[3]),
#                          int(new_box[0]):int(new_box[0])+int(new_box[2])]
#         cv2.namedWindow("trackedROI", cv2.WINDOW_NORMAL)
#         cv2.imshow("trackedROI", crop_img)
#         cv2.waitKey(1)
# =============================================================================
    # draw tracked path
    with open (path_tracker_rois, "r") as tracker_hist_data:
        for line in tracker_hist_data:
            dots = (line.split(", C")[0]).split(", ")
            dots = list(map(float, dots))
            x = (int(dots[0] + dots[2]/2))
            y = (int(dots[1] + dots[3]/2))
            # auto in red
            if line.split(", ")[-1].strip() == "Auto":
                cv2.circle(frame, (x, y), 1, (0,0,255), -1)
            # manual in Orange
            elif line.split(", ")[-1].strip() == "Manual":
                cv2.circle(frame, (x, y), 1, (0,150,255), -1)

# ====  Display FPS on frame  =================================================
#
#     if len(boxes) == 1:
#         cv2.putText(frame, "FPS : " + str(int(fps)), (100, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50, 170, 50), 2)
#
# =============================================================================
    return frame

# Create tracker according to tracker_type
def create_tracker(tracker_type):
    tracker = []
    if tracker_type == 'MIL':
        tracker = cv2.TrackerMIL_create()
    elif tracker_type == 'KCF':
        tracker = cv2.TrackerKCF_create()
    elif tracker_type == 'TLD':
        tracker = cv2.TrackerTLD_create()
    elif tracker_type == 'MEDIANFLOW':
        tracker = cv2.TrackerMedianFlow_create()
    elif tracker_type == 'MOSSE':
        tracker = cv2.TrackerMOSSE_create()
    elif tracker_type == "CSRT":
        tracker = cv2.TrackerCSRT_create()
    return tracker


# return a frame and status, by file name/ video name and frame number
def load_image_from_file_or_video(run_images_from_folder, video_files, frame_number, video):
    if run_images_from_folder:
        if frame_number >= len(video_files):
            ok = False
            return ok, []
        filename = video_files[frame_number]
        # video_folder + str(frame_number) + ".jpg"
        if not os.path.isfile(filename):
            print('file not found: ' + filename)
            ok = False
            return ok, []
        frame = cv2.imread(filename, cv2.IMREAD_COLOR)
        if frame is None:
            print('file not found: ' + filename)
            ok = False
            return ok, []
        ok = True

    else:
        # video.set(cv2.cv2_CAP_PROP_POS_FRAMES, frame_number)
        ok, frame = video.read()
        if not ok:
            print('Cannot read video file')
            sys.exit()

    file_name = filename.split(r"6\DSC_")[-1]
    return ok, frame, file_name


## Return initial bounding box from selection
def get_initial_bounding_box(frame):
    # origin that works!:
#    cv2.namedWindow("SELECT ROI", cv2.WINDOW_NORMAL)
#    bbox = cv2.selectROI("SELECT ROI", frame, True)
#    return bbox

    # muliple trackers:
    # creat a copy of the frame to show selected boxes
    show_selected_frame = frame.copy()
    bboxs = []
    while True:
        cv2.namedWindow("SELECT ROI", cv2.WINDOW_NORMAL)
        bbox = cv2.selectROI("SELECT ROI", show_selected_frame, showCrosshair=True, fromCenter=False)
        if bbox == (0, 0, 0, 0):
            break
        bboxs.append(bbox)
        # drawing the selected boxes on the copy:
        for bbox in bboxs:
            show_selected_frame = cv2.rectangle(show_selected_frame, (bbox[0], bbox[1]), (bbox[0]+bbox[2],bbox[1]+ bbox[3]),
                                                (50, 50, 200) , 2)
            show_selected_frame = cv2.line(show_selected_frame, (bbox[0]+int(bbox[2]/2), bbox[1]), (bbox[0]+int(bbox[2]/2), bbox[1]+ bbox[3]),(50, 50, 200),2)
            show_selected_frame = cv2.line(show_selected_frame, (bbox[0], bbox[1]+int(bbox[3]/2)), (bbox[0]+bbox[2], bbox[1]+int(bbox[3]/2)),(50, 50, 200),2)
    return bboxs

def tracker_loop(frame_to_start, run_images_from_folder, video_files, video,
                   multi_tracker,video_or_folder_name,
                 tracker_types, object_name, output_path, first_tiral,
                 # first_tiral is mine and for difrence between "a" and "w" writing!
                 video_out, colors = get_box_colors()):
    # loop through frames
    i_frame = frame_to_start
    print(i_frame)
    k = 0
    while True:
        try:
            ok, frame, f_name = load_image_from_file_or_video(run_images_from_folder, video_files, i_frame, video)
            # Start timer
            timer = cv2.getTickCount()

            # get updated location of objects in subsequent frames
            # start_time = time.time()  # start time of the loop
            ok, boxes = multi_tracker.update(frame)
            # if lost tracking break
            if not ok:
                print("\nLost it at -", i_frame)
                return i_frame, 112

            # save current rois from all trackers to txt files
            path_tracker_rois = save_result_rois(video_or_folder_name, boxes, [],
                             tracker_types, False,   object_name,
                             f_name, output_path, first_tiral)

            frame_resized  = frame
#            frame_resized = cv2.resize(frame, (width_frame, height_frame))
            frame_with_box = draw_bounding_box(frame_resized, boxes, ok, timer, #ground_truth_bbox,
                                              tracker_types, colors, i_frame,
                                              path_tracker_rois)

            cv2.namedWindow('Tracking', cv2.WINDOW_NORMAL)
            cv2.imshow("Tracking", frame_with_box)
            video_out.write(frame_with_box)

            # Exit if ESC pressed
            k = cv2.waitKey(1) & 0xff
            if k == 27: # Esc key
                print("\nCaught ESC")
                break
            if k == 112: # p key
                print("\nPaused, go do some manual work!\n last one was", i_frame)
                break

            # Update progress bar
            if (i_frame % 10) == 0 or i_frame == 1:
                percent_done = i_frame / len(video_files)
                progress_bar.update_progress_bar(percent_done, str(i_frame))

            i_frame += 1
        except KeyboardInterrupt:
            print("\nCaught Keyboard Interrupt")
            print(i_frame)
            break

        except ValueError:
            break
    return i_frame, k

# Run tracker according to tracking params. Display result on images
def run_tracker_wrapper(tracker_types, run_images_from_folder,
                        video_or_folder_name, frame_to_start,
                        object_name, output_path, first_tiral):
    """ The function runs a few opencv2 trackers on a video (which has previously been split into frames)
        then it saves a video of the results

        Parameters
        ----------
        tracker_types : list
                    a list of the tracker types to run
                    the names should match the types specified in create_tracker funciton
                    example: ['MIL', 'KCF', 'TLD', 'MEDIANFLOW', 'MOSSE', 'CSRT']
        run_images_from_folder : bool
                    if true run on frames what were extraacted from a video, if false run movie.
        video_or_folder_name : str
                    Path to a folder contains videos frames (assumed to be in YUV format).
                    example: 'C:\\ExamplesOfInputs4Testing\\vot2016Simple\\blanket_yuv'
        frame_to_start : int
                    frame to start tracking
                    example: 0
        object_name : str
                    name to add to end of outputs
                    example: 'obj1'
       """

    # Create MultiTracker object
    multi_tracker = cv2.MultiTracker_create()

    # load first frame
    if run_images_from_folder:
        video = []
        video_files = list_images_in_path(video_or_folder_name)
        if video_files == []:
            print("bad file format for imgs in path!, no files found")
            sys.exit()
    else:
        video = cv2.VideoCapture(video_or_folder_name)
        # Exit if video not opened.
        if not video.isOpened():
            print("Could not open video")
            sys.exit()
        run_images_from_folder = []
        video_files = []

    ok, frame, f_name = load_image_from_file_or_video(run_images_from_folder,
                                                      video_files, frame_to_start,
                                                      video)
    if not ok:
        print('Cannot read load_image_from_file_or_video at init')
        sys.exit()
# =============================================================================
#     # resize frame if necessary
#     shape_frame = frame.shape
#     if shape_frame[1] > 1920:
#         AR_frame = float(shape_frame[1]) / float(shape_frame[0])
#         width_frame = 1920
#         height_frame = round(float(width_frame) / AR_frame)
#     else:
#         width_frame = shape_frame[1]
#         height_frame = shape_frame[0]
# =============================================================================
    # Get initial bounding box from user input
#    bbox_init = get_initial_bounding_box(frame)
    init_bboxs = get_initial_bounding_box(frame)
    cv2.destroyAllWindows()
    # Initialize MultiTracker
    for tracker_type in tracker_types:
        for bbox in init_bboxs:
            print(tracker_type)
            multi_tracker.add(create_tracker(tracker_type), frame, bbox)

#    colors = get_box_colors()  # get colors to display on screen

    # set video output for saving
    video_out = create_video_results(video_or_folder_name, frame,   object_name, output_path)

    # save current rois from all trackers to txt files
    path_tracker_rois = save_result_rois(video_or_folder_name, [], init_bboxs,
                                         tracker_types, True,   object_name,
                                         f_name, output_path, first_tiral)

    i_frame = frame_to_start
    while i_frame < len(video_files):
        # Auto tracking
        i_frame, k  = tracker_loop(i_frame, run_images_from_folder, video_files, video,
                                   multi_tracker,video_or_folder_name,
                                   tracker_types, object_name, output_path, first_tiral,
                                   video_out, colors = get_box_colors())
        # Esc
        if k == 27:
            break
        # Manual tracking
        elif k == 112: # p key
            if run_images_from_folder == True:
                i_frame, manual_k = manual_tracking.loop_through_imgs(video_or_folder_name,
                                                                      path_tracker_rois, i_frame,
                                                                      video_out)
            else:
                print("Nope... can't track manualy with video")
                break
            # back to Auto tracking
            if manual_k == 27: #if Esc Key from the tracker continue Auto tracker

                multi_tracker = cv2.MultiTracker_create()

                ok, frame, f_name = load_image_from_file_or_video(run_images_from_folder,
                                                      video_files, i_frame,
                                                      video)
                # Get initial bounding box from user input
                bbox_init = get_initial_bounding_box(frame)
                cv2.destroyAllWindows()
                # Initialize MultiTracker
                for tracker_type in tracker_types:
                    multi_tracker.add(create_tracker(tracker_type), frame, bbox_init)
                path_tracker_rois = save_result_rois(video_or_folder_name, [], bbox_init,
                                                     tracker_types, True,   object_name,
                                                     f_name, output_path, first_tiral = False)

    percent_done = i_frame / len(video_files)
    progress_bar.update_progress_bar(percent_done, str(i_frame))
    print('\nreached end of video files: frame_number=' + str(i_frame))

    video_out.release()
    cv2.destroyAllWindows()
#%%
def main():
    #%%
    run_images_from_folder = True
    frame_to_start = 0  # in the range: [0, number of frames in video-1]
    first_tiral = True # in order to continue from last point

    # Choose which trackers to run
    tracker_type_list = ['CSRT']#, 'KCF']#, 'TLD', 'MEDIANFLOW','MIL', 'MOSSE']

    # path with videos or files
    video_or_folder_name =  r"C:\Users\YasmineMnb\Desktop\pics_feb\1\side_croped_2"
    output_path = r"Tracked____test" # only LOCAL file name! not full path
    object_name = '2' #tip name

    outfolder = os.path.dirname(video_or_folder_name) + "\\" + output_path

    if os.path.isdir(outfolder):
        print("that folder already exists! are you sure you want to continue?")
        ans = input("y/n? ")
        if ans == "n":
            sys.exit()

    print("\nstart tracking: ")
    run_tracker_wrapper(tracker_type_list, run_images_from_folder,
                        video_or_folder_name, frame_to_start,
                        object_name, output_path,
                        first_tiral)


#%%
if __name__ == "__main__":
    main()
