from time import sleep
from multiprocessing import Process
from subprocess import Popen, call
import pickle
import os
import signal
import cv2 as cv
from gtts import gTTS
import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
from OCR.SceneOCR import SceneOCR
from OCR.DocScanner import DocScanner 
from OCR.DocOCR import DocOCR
from SeneDescribe.Depth import SceneDescribe
import os
from audioplayer import AudioPlayer
from playsound import playsound
import time




image_path="InputImages/camera_image_2.jpeg"
output_image_path="OutputImages/output_camera_image_2.jpeg"

#scene ocr object
text_detection_model_path="Models/frozen_east_text_detection.pb";
text_recognition_model_path="Models/crnn.onnx";
detector_model = cv.dnn.readNet(text_detection_model_path)
recognizer_model = cv.dnn.readNet(text_recognition_model_path)


scene_ocr=SceneOCR(detector_model,recognizer_model,image_path)

#Describe Scene object
Depth_model_path="SeneDescribe/Models/lite-model_midas_v2_1_small_1_lite_1.tflite"
Object_detection_model_path="SeneDescribe/Models/efficientdet_lite0.tflite"

scene_desc=SceneDescribe(Depth_model_path , Object_detection_model_path)

#doc_to_string_stuff
doc_scan=DocScanner()
doc_ocr=DocOCR()



cycle_pin=11
select_pin=13
cancel_pin=15

#172 is a value with focus from 30 cm to infinity
value = (195<<4) & 0x3ff0
dat1 = (value>>8)&0x3f
dat2 = value & 0xf0

#os.system("i2cset -y 22 0x0c %d %d" % (dat1,dat2))

GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BOARD) # Use physical pin numbering

GPIO.setup(cycle_pin, GPIO.IN,GPIO.PUD_UP) # Set pin nth to be an input pin and set initial value to be pulled low (off)
GPIO.setup(select_pin, GPIO.IN,GPIO.PUD_UP) # Set pin nth to be an input pin and set initial value to be pulled low (off)
GPIO.setup(cancel_pin, GPIO.IN,GPIO.PUD_UP) # Set pin nth to be an input pin and set initial value to be pulled low (off)


GPIO.add_event_detect(cycle_pin,GPIO.RISING,bouncetime=500) # Setup event on pin 10 rising edge
GPIO.add_event_detect(select_pin,GPIO.RISING,bouncetime=500) # Setup event on pin 10 rising edge
GPIO.add_event_detect(cancel_pin,GPIO.RISING,bouncetime=500) # Setup event on pin 10 rising edge


print("models Loaded")
Popen("mpg321 DocumentOCRMode.mp3", shell=True).wait()


def tts(text):
    if len(text) < 3:
        return
    s = gTTS(text)
    s.save('tts.mp3')
    time.sleep(0.2)




class SubprocessObserver:
    def __init__(self):
        self.processes = []
    
    # Create a subprocess
    def create(self, command):
        p = Popen(command, shell=True, preexec_fn=os.setpgrp)
        self.processes.append(p.pid)
        print(self.processes)
        pickle.dump(self.processes,open('test.p','wb'))
        return p

    
    # Kill and remove all the subprocesses
    def kill(self):
        self.processes = pickle.load(open('test.p', 'rb'))
        for pid in self.processes:
            try:
                os.killpg(os.getpgid(pid), signal.SIGTERM)
            except ProcessLookupError:
                print("Process is already terminated")
        self.processes = []
        pickle.dump(self.processes,open('test.p','wb'))
        
    def isAlive(self):
        self.processes = pickle.load(open('test.p', 'rb'))
        for pid in self.processes:
            try:
                os.getpgid(pid)
            except ProcessLookupError:
                self.processes.remove(pid)
        pickle.dump(self.processes,open('test.p','wb'))
        return len(self.processes) > 0
        

class State:
    Count = 3
    DocOCR = 0
    SceneOCR = 1
    SceneDesc = 2
    
    mp3dict={0:"DocumentOCRMode.mp3",1:"SceneOCRMode.mp3",2:"DescribeSceneMode.mp3"}
    
    @classmethod
    def name(cls, state):
        if state == State.DocOCR:
            return "DocOCR"
        if state == State.SceneOCR:
            return "SceneOCR"
        if state == State.SceneDesc:
            return "SceneDesc"
        return "Invalid"
        
    @classmethod
    def play(cls, state):
        Popen(f"mpg321 {State.mp3dict[state]}", shell=True).wait()
        

class ButtonHandler:
    def __init__(self):
        self.state = State.DocOCR
        self.currProc = Process(target=self.performDocOcr)
        self.observer = SubprocessObserver()
        
    def create(self, command):
        return self.observer.create(command)
        
    def performDocOcr(self):
        cmd = "libcamera-jpeg -o InputImages/camera_image_2.jpeg -t 1000 --width 2500 --height 2500"
        p = self.create(cmd)
        p.wait()
        #creating a scan of the input image
        crop_status,cropped_image = doc_scan.scan(path=image_path)
        
        #save the image
        cv.imwrite(output_image_path,cropped_image)
        
        #sometimes exact corners cannot be found
        if(crop_status == 0):
            print("couldnt find exact page to crop")

        string = doc_ocr.ocr(imagePath='OutputImages/output_camera_image_2.jpeg')
            
        if(len(string) > 3):
            print(f"string = {string}")
            tts(string)
            self.create("mpg321 tts.mp3")
        else:
            print(f"No text detected")
            self.create("mpg321 noText.mp3")
    
    def performSceneOcr(self):        
        cmd = "libcamera-jpeg -o InputImages/camera_image_2.jpeg -t 1000 --width 960 --height 960"
        p = self.create(cmd)
        p.wait()
        string = scene_ocr.ocr()
        if(len(string) > 3):
            print(f"string = {string}")
            tts(string)
            self.create("mpg321 tts.mp3")
        else:
            print(f"No text detected")
            self.create("mpg321 noText.mp3")
    
    def performSceneDesc(self):        
        cmd = "libcamera-jpeg -o InputImages/camera_image_2.jpeg -t 1000 --width 960 --height 960"
        p = self.create(cmd)
        p.wait()
        string = scene_desc.describe(cv.imread("InputImages/camera_image_2.jpeg"))
        if(len(string) > 3):
            print(f"string = {string}")
            tts(string)
            self.create("mpg321 tts.mp3")
        else:
            print(f"No text detected")
            self.create("mpg321 noText.mp3")

    
    def kill(self):
        self.observer.kill()
        
    def cycle(self):
        if self.currProc.is_alive() or self.observer.isAlive():
            return
        self.state = (self.state + 1) % State.Count
        State.play(self.state)
        
    def select(self):
        if self.currProc.is_alive() or self.observer.isAlive():
            return
        
        if self.state == State.DocOCR:
            self.currProc = Process(target=self.performDocOcr)
        elif self.state == State.SceneOCR:
            self.currProc = Process(target=self.performSceneOcr)
        elif self.state == State.SceneDesc:
            self.currProc = Process(target=self.performSceneDesc)

        self.currProc.start()
    
    def cancel(self):
        self.kill()
        if self.currProc.is_alive():
            self.currProc.terminate()

    
class Test:
    # Cycle test
    @classmethod
    def cycleTest(cls, handler):
        print(f"Currently in {State.name(handler.state)} mode")
        print("Cycle once")
        handler.cycle()

    # Select and Cancel test
    @classmethod
    def selectAndCancelTest(cls, handler):
        print(f"Started {State.name(handler.state)} process")
        handler.select()
        sleep(1)
        handler.cancel()
        print("Cycle once")
        handler.cycle()



if __name__ == "__main__":
    handler = ButtonHandler()

    while True:
        if GPIO.event_detected(cycle_pin):
            print('cycle_pin_pushed')
            handler.cycle()
            print(f"Currently in {State.name(handler.state)} mode")

        if GPIO.event_detected(select_pin):
            print(f"Currently in {State.name(handler.state)} mode")
            print('select_pin_pushed')
            handler.select()

        if GPIO.event_detected(cancel_pin):
            print('cancel_pin_pushed')
            handler.cancel()

    GPIO.cleanup() # Clean up
