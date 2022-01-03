import cv2 as cv
from gtts import gTTS
import os,sys,subprocess
import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
from OCR.SceneOCR import SceneOCR


text_detection_model_path="/home/pi/Desktop/GitHub/OurVision/TejasTextDetection/frozen_east_text_detection.pb";
text_recognition_model_path="/home/pi/Desktop/GitHub/OurVision/TejasTextDetection/crnn.onnx";
detector_model = cv.dnn.readNet(text_detection_model_path)
recognizer_model = cv.dnn.readNet(text_recognition_model_path)
image_path="/home/pi/Desktop/GitHub/OurVision/TejasTextDetection/camera_image_2.jpeg"

obj=SceneOCR(detector_model,recognizer_model,image_path)

print("models Loaded")
	
		
def button_callback(channel):
	print("hello")
	
	
	cmd = "libcamera-jpeg -o /home/pi/Desktop/GitHub/OurVision/TejasTextDetection/camera_image_2.jpeg -t 1500 --width 960 --height 960"
	returned_value = subprocess.call(cmd,shell=True)  
	print(f"return value{returned_value}")
	if (returned_value==0):
		str=obj.ocr()
		if(len(str)>3):
			print({f"string======>>> {str}"})
			tts = gTTS(str)
			tts.save('hello.mp3')
			subprocess.call("mpg321 hello.mp3",shell=True)
		else:
			print({f"No Text Detected"})
			tts = gTTS("no text detected")
			tts.save('noText.mp3')
			subprocess.call("mpg321 noText.mp3",shell=True)
			
 
GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 10 to be an input pin and set initial value to be pulled low (off)

GPIO.add_event_detect(10,GPIO.FALLING,callback=button_callback,bouncetime=1000) # Setup event on pin 10 rising edge

message = input("Press enter to quit\n\n") # Run until someone presses enter

GPIO.cleanup() # Clean up


