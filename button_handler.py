from multiprocessing import Process
from observer import SubprocessObserver
from state import State
from paths import *
from models import *
from tts import tts

class ButtonHandler:
    def __init__(self):
        self.state = State.DocOCR
        self.currProc = Process(target=self.perform_doc_ocr)
        self.observer = SubprocessObserver()
        
    def create(self, command):
        return self.observer.create(command)
        
    def perform_doc_ocr(self):
        cmd = "libcamera-jpeg -o " + INPUT_IMAGE_PATH + " -t 1000 --width 2500 --height 2500"
        p = self.create(cmd)
        p.wait()
        # Creating a scan of the input image
        crop_status,cropped_image = doc_scan.scan(path=INPUT_IMAGE_PATH)
        
        # Save the image
        cv.imwrite(OUTPUT_IMAGE_PATH,cropped_image)
        
        # Sometimes exact corners cannot be found
        if(crop_status == 0):
            print("couldnt find exact page to crop")

        string = doc_ocr.ocr(imagePath=OUTPUT_IMAGE_PATH)
            
        if(len(string) > 3):
            print(f"string = {string}")
            tts(string)
            self.create("mpg321 ./audios/tts.mp3")
        else:
            print(f"No text detected")
            self.create("mpg321 ./audios/noText.mp3")
    
    def perform_scene_ocr(self):        
        cmd = "libcamera-jpeg -o " + INPUT_IMAGE_PATH + " -t 1000 --width 960 --height 960"
        p = self.create(cmd)
        p.wait()
        string = scene_ocr.ocr()
        if(len(string) > 3):
            print(f"string = {string}")
            tts(string)
            self.create("mpg321 ./audios/tts.mp3")
        else:
            print(f"No text detected")
            self.create("mpg321 ./audios/noText.mp3")
    
    def perform_scene_desc(self):        
        cmd = "libcamera-jpeg -o " + INPUT_IMAGE_PATH + "-t 1000 --width 960 --height 960"
        p = self.create(cmd)
        p.wait()
        string = scene_desc.describe(cv.imread(INPUT_IMAGE_PATH))
        if(len(string) > 3):
            print(f"string = {string}")
            tts(string)
            self.create("mpg321 ./audios/tts.mp3")
        else:
            print(f"No text detected")
            self.create("mpg321 ./audios/noText.mp3")

    
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
            self.currProc = Process(target=self.perform_doc_ocr)
        elif self.state == State.SceneOCR:
            self.currProc = Process(target=self.perform_scene_ocr)
        elif self.state == State.SceneDesc:
            self.currProc = Process(target=self.perform_scene_desc)

        self.currProc.start()
    
    def cancel(self):
        self.kill()
        if self.currProc.is_alive():
            self.currProc.terminate()