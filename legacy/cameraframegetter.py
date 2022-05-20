
import time

from picamera.array import PiRGBArray
from picamera import PiCamera

import cv2


def GetFrame():
	camera = PiCamera()
	camera.resolution = (900, 900)
	camera.framerate = 32
	rawCapture = PiRGBArray(camera, size=(900, 900))
	# allow the camera to warmup
	time.sleep(0.1)
	# capture frames from the camera
	t_end = time.time() + 10 #8seconds
	for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
		# grab the raw NumPy array representing the image, then initialize the timestamp
		# and occupied/unoccupied text
		image = frame.array
		# show the frame
		cv2.imshow("Frame", image)
		key = cv2.waitKey(1) & 0xFF
		# clear the stream in preparation for the next frame
		rawCapture.truncate(0)
		# if the `q` key was pressed, break from the loop
		if time.time() > t_end:
			cv2.destroyWindow("Frame") 
			break


	# allow the camera to warmup
	time.sleep(0.1)
	start = time.time()
	# grab an image from the camera
	camera.capture(rawCapture, format="bgr")
	image = rawCapture.array
	# display the image on screen and wait for a keypress
	cv2.imshow("Image", image)
	cv2.waitKey(1000)
	cv2.destroyAllWindows()
	
	return image

GetFrame()
