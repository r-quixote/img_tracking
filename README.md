# cropping for folder, convert imgs to video, tracker2.1 


keep in mind that this was written to be used with an open terminal/from within spyder
(while seeing the printed msgs from the script)
------------
##### need to add *how to use tracker* section here

##### How to:

![tip_with_track](examples/tip%20with%20track.png)


------------

##### whats new:
* tracker can be paused with 'p' for manual tracking *(of one point only!)* .
* several types of tracker can be used at the same time.
* several initial rois can be selected at begining of tracking
* added timestamp to img cropping
* added simple file choosing dialog to cropping - needs fine tuning

------------
**2DO:**
- [X] ~~add tracking for second point in order to track angle between 2 points~~
- [ ] can't go to manual when tracking multiple points
	(in general manual still needs all sorts of work...)
- [ ] add run from terminal
	- [ ] finish more robust file dialog for cropping.py  
	- [ ] add file dialog for tracker_21.py
	- [ ] add file dialog for im2vid_v2.py
- [ ] file name indepence (trial with imgs from PI/webcam/other name format)
	- [ ] figure out filename independent way to find timestamp

	
**2DO - not really important:**
- [X] add timestamp to crop last img
- [ ] add brightness controll to img_procesing.py - maybe auto brightness correction for imgs with natural lighting
- [ ] clean up progress bar mess
- [ ] add help section for img_procesing
- [ ] add cropping several parts to cropping.py


_**2DO someday (maybe...):**_
- [ ] add GUI (browser based app?)
- [ ] linux / Raspberry PI compatible?

------------
# suggestions are more then welcome!

wishlist:
- [ ]
- [ ]
- [ ]
- [ ]
