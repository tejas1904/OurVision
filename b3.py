import cv2 as cv
from gtts import gTTS
import os,sys,subprocess
import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
from OCR.SceneOCR import SceneOCR
from OCR.DocScanner import DocScanner 
from OCR.DocOCR import DocOCR
from SeneDescribe.Depth import SceneDescribe
import os
from audioplayer import AudioPlayer
from playsound import playsound


image_path="InputImages/camera_image_2.jpeg"
output_image_path="OutputImages/output_camera_image_2.jpeg"

#scene ocr object
text_detection_model_path="Models/frozen_east_text_detection.pb";
text_recognition_model_path="Models/crnn.onnx";
detector_model = cv.dnn.readNet(text_detection_model_path)
recognizer_model = cv.dnn.readNet(text_recognition_model_path)


obj=SceneOCR(detector_model,recognizer_model,image_path)

#Describe Scene object
Depth_model_path="SeneDescribe/Models/lite-model_midas_v2_1_small_1_lite_1.tflite"
Object_detection_model_path="SeneDescribe/Models/efficientdet_lite0.tflite"

obj2=SceneDescribe(Depth_model_path , Object_detection_model_path)

#doc_to_string_stuff

obj3=DocScanner()
obj4=DocOCR()




print("models Loaded")
	
		
def perform_scene_ocr():
	print("hello")
	
	cmd = "libcamera-jpeg -o InputImages/camera_image_2.jpeg -t 1 --width 960 --height 960"
	returned_value = subprocess.call(cmd,shell=True)
	print(f"return value{returned_value}")
	if (returned_value==0):
		string=obj.ocr()
		if(len(string)>3):
			print({f"string======>>> {string}"})
			try:
				tts = gTTS(string)
				tts.save('hello.mp3')
				#subprocess.call("mpg321 hello.mp3",shell=True)
				player.play_song("hello.mp3")
			except:
				print("no internet for gtts")
				
		else:
			print({f"No Text Detected"})
			try:
				AudioPlayer('noText.mp3').play(block=True)
				#subprocess.call("mpg321 noText.mp3",shell=True)
				
			except:
				print("no internet for gtts")

def perform_scene_describe():
	print("hello")
	
	
	cmd = "libcamera-jpeg -o InputImages/camera_image_2.jpeg -t 1  --width 960 --height 960"
	returned_value = subprocess.call(cmd,shell=True)  
	print(f"return value{returned_value}")
	if (returned_value==0):
		img=cv.imread("InputImages/camera_image_2.jpeg")
		string=obj2.describe(img)
		if(len(string)>3):
			print({f"string======>>> {string}"})
			try:
				tts = gTTS(string)
				tts.save('hello.mp3')
				#subprocess.call("mpg321 hello.mp3",shell=True)
				playsound('hello.mp3')
				print("done")
			except:
				print("no internet for gtts")
				
		else:
			print({f"No Text Detected"})
			try:
				playsound('noText.mp3')
				#subprocess.call("mpg321 noText.mp3",shell=True)
				
			except:
				print("no internet for gtts")

def perform_doc_to_string():
	
	cmd = "libcamera-jpeg -o InputImages/camera_image_2.jpeg -t 1 --width 2500 --height 2500"
	returned_value = subprocess.call(cmd,shell=True)
	print(f"return value{returned_value}")
	if (returned_value==0):
		#creating a scan of the input image
		crop_status,cropped_image = obj3.scan(path=image_path)
		
		#save the image
		cv.imwrite(output_image_path,cropped_image)
		
		#sometimes exact corners cannot be found
		if(crop_status == 0):
			print("couldnt find exact page to crop")
		

		string = obj4.ocr(imagePath='OutputImages/output_camera_image_2.jpeg')
		
		if(len(string)>3):
			print({f"string======>>> {string}"})
			try:
				tts = gTTS(string)
				tts.save('hello.mp3')
				#subprocess.call("mpg321 hello.mp3",shell=True)
				AudioPlayer('hello.mp3').play(block=True)
			except:
				print("no internet for gtts")
				
		else:
			print({f"No Text Detected"})
			try:
				AudioPlayer('noText.mp3').play(block=True)
				#subprocess.call("mpg321 noText.mp3",shell=True)
				player.play_song("noText.mp3")
			except:
				print("no internet for gtts")
		
		
from multiprocessing import Process
doc_ocr = Process(target=perform_doc_to_string)
scene_ocr = Process(target=perform_scene_ocr)
scene_desc = Process(target=perform_scene_describe)

cycle_pin=11
select_pin=13
cancel_pin=15

#172 is a value with focus from 30 cm to infinity
value = (195<<4) & 0x3ff0
dat1 = (value>>8)&0x3f
dat2 = value & 0xf0
os.system("i2cset -y 22 0x0c %d %d" % (dat1,dat2))

GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BOARD) # Use physical pin numbering

GPIO.setup(cycle_pin, GPIO.IN,GPIO.PUD_UP) # Set pin nth to be an input pin and set initial value to be pulled low (off)
GPIO.setup(select_pin, GPIO.IN,GPIO.PUD_UP) # Set pin nth to be an input pin and set initial value to be pulled low (off)
GPIO.setup(cancel_pin, GPIO.IN,GPIO.PUD_UP) # Set pin nth to be an input pin and set initial value to be pulled low (off)


GPIO.add_event_detect(cycle_pin,GPIO.RISING,bouncetime=500) # Setup event on pin 10 rising edge
GPIO.add_event_detect(select_pin,GPIO.RISING,bouncetime=500) # Setup event on pin 10 rising edge
GPIO.add_event_detect(cancel_pin,GPIO.RISING,bouncetime=500) # Setup event on pin 10 rising edge

curr = None



## Button Handler 

class State:
	Count = 3
	SceneOCR = 0
	DocOCR = 1
	SceneDescribe = 2
	

class ButtonHandler:
	def __init__(self):
		self.mp3dict={1:"DocumentOCRMode.mp3",0:"SceneOCRMode.mp3",2:"DescribeSceneMode.mp3"}
		self.state = State.SceneOCR
		self.curr_proc = Process(target=perform_scene_describe)
		
		print(self.state)
		AudioPlayer(self.mp3dict[self.state]).play(block=True)
		
	def up(self):
		
		
		
		self.state = (self.state + 1) % State.Count
		print(self.state)
		AudioPlayer(self.mp3dict[self.state]).play(block=True)
		
	def start(self):
		if(self.curr_proc.is_alive()):
			return
		if self.state == State.SceneOCR:
			self.curr_proc = Process(target=perform_scene_ocr)
		if self.state == State.SceneDescribe:
			self.curr_proc = Process(target=perform_scene_describe)
		if self.state == State.DocOCR:
			self.curr_proc = Process(target=perform_doc_to_string)
			
		print(self.state)
		AudioPlayer(self.mp3dict[self.state]).play(block=True)
		
		self.curr_proc.start()
	
	def terminate(self):
		self.curr_proc.kill()
		self.curr_proc.terminate()


if __name__ == "__main__":
	handler = ButtonHandler()

	while True:
		if GPIO.event_detected(cycle_pin):
			print('cycle_pin_pushed')
			handler.up()
			
		if GPIO.event_detected(select_pin):
			print('select_pin_pushed')
			handler.start()
			
		if GPIO.event_detected(cancel_pin):
			print('cancel_pin_pushed')
			handler.terminate()
				
	GPIO.cleanup() # Clean up

"""
while True:
	if GPIO.event_detected(cycle_pin):
		print('cycle_pin_pushed')
		curr = scene_ocr
		scene_ocr.start()
		
	if GPIO.event_detected(select_pin):
		print('select_pin_pushed')
		curr = scene_desc
		scene_desc.start() 
	if GPIO.event_detected(cancel_pin):
		print('cancel_pin_pushed')
		#write the exit code
		if curr:
			curr.terminate()
			
	if not scene_ocr.is_alive() and not scene_desc.is_alive():
		curr = None
			
GPIO.cleanup() # Clean up
"""




