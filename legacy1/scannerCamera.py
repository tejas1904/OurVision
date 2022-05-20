import cv2
from PIL import Image
from scanner import DocScanner
import time

import pytesseract as pt
pt.pytesseract.tesseract_cmd = '/usr/bin/tesseract'

from picamera.array import PiRGBArray
from picamera import PiCamera


def ocr(image):
    a = pt.image_to_string(image)

    lines = a.split("\n")
    newLines = []
    for i in lines:
        if i != ' ' and i != '  ' and i != '   ' and i != '' and i != "    ":
            newLines.append(i)
            
    finalString = ""
    for i in newLines:
        finalString += i + ".\n"
        
    return finalString

def image_processing(image):
    from PIL import Image, ImageEnhance, ImageFilter

    #read the image
    im = Image.fromarray(image)
    print("3.1 extracted image")

    enhancer = ImageEnhance.Contrast(im)

    factor = 1 #gives original image
    im_output = enhancer.enhance(factor)
    print("3.2 enhanced image")

    factor = 0.5 #decrease constrast
    im_output = enhancer.enhance(factor)
    print("3.3 decreased contrast")

    factor = 1.5 #increase contrast
    im_output = enhancer.enhance(factor)
    print("3.4 increased contrast")


    x = im.convert('L')
    im_output = x.point(lambda x: 0 if x<128 else 255, '1')
    print("3.5 segmented image")
    
    #im_output.filter(ImageFilter.MinFilter(25))
    #im_output.filter(ImageFilter.MaxFilter(9))
    #print("3.6 image dilated and eroded")
    return im_output




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

print("1. image read")
# scan the image
scanned_image = DocScanner().scan(image)

cv2.imshow("Frame3",scanned_image)
cv2.waitKey(3000) & 0xFF

print("2. image scanned")
processed_scanned_image = image_processing(scanned_image)



print("3. image processed")

ocr_string = ocr(processed_scanned_image)

print("time taken = ", start - time.time())
print("4. image ocr'ed")
print("\n\n\n OCR String:\n")
print(ocr_string)

# text to speech here
