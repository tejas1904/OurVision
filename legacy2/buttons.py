import cv2 as cv
from gtts import gTTS
import os,sys,subprocess
import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
from OCR.SceneOCR import SceneOCR
from SceneDescribe.Depth import SceneDescribe

#scene ocr object
text_detection_model_path="Models/frozen_east_text_detection.pb";
text_recognition_model_path="Models/crnn.onnx";
detector_model = cv.dnn.readNet(text_detection_model_path)
recognizer_model = cv.dnn.readNet(text_recognition_model_path)
image_path="/home/pi/Desktop/GitHub/OurVision/TejasTextDetection/camera_image_2.jpeg"

obj=SceneOCR(detector_model,recognizer_model,image_path)

#Describe Scene object
Depth_model_path="SceneDescribe/Models/lite-model_midas_v2_1_small_1_lite_1.tflite"
Object_detection_model_path="SceneDescribe/Models/efficientdet_lite0.tflite"

obj2=SceneDescribe(Depth_model_path , Object_detection_model_path)


print("models Loaded")
	
		
def perform_scene_ocr():
	print("hello")
	
	
	cmd = "libcamera-jpeg -o TejasTextDetection/camera_image_2.jpeg -t 1500 --width 960 --height 960"
	returned_value = subprocess.call(cmd,shell=True)  
	print(f"return value{returned_value}")
	if (returned_value==0):
		str=obj.ocr()
		if(len(str)>3):
			print({f"string======>>> {str}"})
			try:
				tts = gTTS(str)
				tts.save('hello.mp3')
				subprocess.call("mpg321 hello.mp3",shell=True)
			except:
				print("no internet for gtts")
				
		else:
			print({f"No Text Detected"})
			try:
				tts = gTTS("no text detected")
				tts.save('noText.mp3')
				subprocess.call("mpg321 noText.mp3",shell=True)
			except:
				print("no internet for gtts")

def perform_scene_describe():
	print("hello")
	
	
	cmd = "libcamera-jpeg -o TejasTextDetection/camera_image_2.jpeg -t 1500 --width 960 --height 960"
	returned_value = subprocess.call(cmd,shell=True)  
	print(f"return value{returned_value}")
	if (returned_value==0):
		img=cv.imread("TejasTextDetection/camera_image_2.jpeg")
		str=obj2.describe(img)
		if(len(str)>3):
			print({f"string======>>> {str}"})
			try:
				tts = gTTS(str)
				tts.save('hello.mp3')
				subprocess.call("mpg321 hello.mp3",shell=True)
			except:
				print("no internet for gtts")
				
		else:
			print({f"No Text Detected"})
			try:
				tts = gTTS("no text detected")
				tts.save('noText.mp3')
				subprocess.call("mpg321 noText.mp3",shell=True)
			except:
				print("no internet for gtts")
	

GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 10 to be an input pin and set initial value to be pulled low (off)

GPIO.add_event_detect(10,GPIO.FALLING,bouncetime=1000) # Setup event on pin 10 rising edge

while True:
	if GPIO.event_detected(10):
		#perform_scene_ocr()
		perform_scene_describe() 


GPIO.cleanup() # Clean up



