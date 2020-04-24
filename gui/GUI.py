# -*- coding: utf-8 -*-
"""
Created on Tue Aug 27 15:49:29 2019

@author: Roni
"""
#%%
import tkinter as tk

from tkinter import ttk
import PIL.Image, PIL.ImageTk
from tkinter import filedialog, messagebox
import cv2
import sys

#import img_procesing

def popupmsg(msg):
    def canceled(popup_window):
        popup_window.destroy()
        try: sys.exit()
        except: raise Exception ("Error")
    popup = tk.Tk()
    popup.wm_title("!")
    popup.lift()
    popup.attributes("-topmost", 1)
    popup.after_idle(popup.attributes,'-topmost',False)
    label = ttk.Label(popup, text=msg, font=20)
#    label.pack(side="top", fill="x", pady=20, padx=10)
    label.grid(row=0, column=0, columnspan=2)
    B1 = ttk.Button(popup, text="Okay", command = popup.destroy)
    B1.grid(row=1, column=0, columnspan=1)
#    B1 = ttk.Button(popup, text="Cancel (!)", command = lambda popup.destroy)
    B2 = ttk.Button(popup, text="Cancel (!)", command = lambda: canceled(popup))
    B2.grid(row=1, column=1, columnspan=1)
#    popup.geometry("100x60")
    popup.mainloop()
#    popup.destroy()


def open_simple_filedialog(msg):
    root = tk.Tk()

    root.lift()
    root.attributes("-topmost", True)
    root.withdraw() # we don't want a full GUI, so keep the root window from appearing
    root.focus_force()
    ok = messagebox.askokcancel("msgbox", msg, master = root)
    # show an "Open" dialog box and return the path to the selected file
    if not ok:
        return '', ok
    filename = filedialog.askdirectory(parent=root, initialdir = "/", title = "Select file") # initialdir=data_dir
    root.destroy()
    return filename, ok

def open_file_save_dialog(msg):
    root = tk.Tk()
    root.lift()
    root.attributes("-topmost", True)
    root.withdraw() # we don't want a full GUI, so keep the root window from appearing
    root.focus_force()
    ok = messagebox.askokcancel("msgbox", msg, master = root)
    # show an "Open" dialog box and return the path to the selected file
    if not ok:
        return '', ok
    filename = filedialog.asksaveasfilename(parent=root, initialdir = "/",title = "Select file", filetypes = (("avi video","*.avi"),("all files","*.*")))
    root.destroy()
    return filename, ok


def filedialog_loop(msg):
    file_path = ""
    while True:
        file_path, ok = open_simple_filedialog(msg)
        if not ok:
            try: sys.exit()
            except: raise Exception ("You Cancled!")
            break
        if file_path != "":
            break

    return file_path

#%%
def select_image():
	# grab a reference to the image panels
	global panelA, panelB

	# open a file chooser dialog and allow the user to select an input
	# image
	path = filedialog.askopenfilename()

    # ensure a file path was selected
	if len(path) > 0:
		# load the image from disk, convert it to grayscale, and detect
		# edges in it
		image = cv2.imread(path)
		gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
		edged = cv2.Canny(gray, 50, 100)

		# OpenCV represents images in BGR order; however PIL represents
		# images in RGB order, so we need to swap the channels
		PIL_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

		# convert the images to PIL format...
		image = Image.fromarray(image)
		edged = Image.fromarray(edged)

		# ...and then to ImageTk format
		image = ImageTk.PhotoImage(image)
		edged = ImageTk.PhotoImage(edged)

		# if the panels are None, initialize them
		if panelA is None or panelB is None:
			# the first panel will store our original image
			panelA = tk.Label(image=image)
			panelA.image = image
			panelA.pack(side="left", padx=10, pady=10)

			# while the second panel will store the edge map
			panelB = tk.Label(image=edged)
			panelB.image = edged
			panelB.pack(side="right", padx=10, pady=10)

		# otherwise, update the image panels
		else:
			# update the pannels
			panelA.configure(image=image)
			panelB.configure(image=edged)
			panelA.image = image
			panelB.image = edged

def main():
    # initialize the window toolkit along with the two image panels
    root = tk.Tk()
    panelA = None
    panelB = None

    # create a button, then when pressed, will trigger a file chooser
    # dialog and allow the user to select an input image; then add the
    # button the GUI
    btn = tk.Button(root, text="Select an image", command=select_image)
    btn.pack(side="bottom", fill="both", expand="yes", padx="10", pady="10")

    # kick off the GUI
    root.mainloop()
#%%
def sec_main():
    import tkinter as tk
    from tkinter import ttk
    import PIL.Image, PIL.ImageTk

    LARGE_FONT= ("Verdana", 12)


    class my_app(tk.Tk):

        def __init__(self, *args, **kwargs):

            tk.Tk.__init__(self, *args, **kwargs)

            tk.Tk.wm_title(self, "img analysis")

            container = tk.Frame(self)

            container.pack(side="top", fill="both", expand = True)

            container.grid_rowconfigure(0, weight=1)
            container.grid_columnconfigure(0, weight=1)

            self.frames = {}

            for F in (StartPage, PageOne):

                frame = F(container, self)

                self.frames[F] = frame

                frame.grid(row=0, column=0, sticky="nsew")

            self.show_frame(StartPage)

        def show_frame(self, cont):

            frame = self.frames[cont]
            frame.tkraise()


    class StartPage(ttk.Frame):

        def __init__(self, parent, controller):
            tk.Frame.__init__(self,parent)
            label = ttk.Label(self, text="Start Page", font=LARGE_FONT)
            label.pack(pady=10,padx=10)

            button = ttk.Button(self, text="Visit Page 1",
                                command=lambda: controller.show_frame(PageOne))
            button.pack()

            button1 = ttk.Button(self, text="load img",
                                command=load_file)
            button1.pack()

    def load_file():
        path = tk.filedialog.askdirectory()
        print( path)

    def show_cv_img(cv_img):
        # Get the image dimensions (OpenCV stores image data as NumPy ndarray)
        height, width, no_channels = cv_img.shape
        # Create a canvas that can fit the above image
        canvas = tk.Canvas(window, width = width, height = height)
        canvas.pack()

    class PageOne(tk.Frame):

        def __init__(self, parent, controller):
            tk.Frame.__init__(self, parent)
            label = ttk.Label(self, text="Page One!!!", font=LARGE_FONT)
            label.pack(pady=10,padx=10)

            button1 = ttk.Button(self, text="Back to Home",
                                command=lambda: controller.show_frame(StartPage))
            button1.pack()




    app = my_app()
    app.geometry("800x600")
    app.mainloop()