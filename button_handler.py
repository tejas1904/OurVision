from multiprocessing import Process
from observer import SubprocessObserver
from state import State
from paths import *
from models import *
from tts import tts, checkInternet,blurCheck
from time import sleep
from audio import play_audio
from saveimage import capture_write as capture
import cv2
usecam = True
class ButtonHandler:
    def __init__(self):
        self.state = State.DocOCR
        self.currProc = Process(target=self.perform_doc_ocr)
        self.observer = SubprocessObserver()
        self.language = 'kn'
    def create(self, command):
        return self.observer.create(command)
    
    def start_sound(self):
        return "sudo mpg321 ./audios/start_tts_sound.mp3"
    def end_sound(self):
        return "sudo mpg321 ./audios/end_tts_sound.mp3"

    def perform_doc_ocr(self):
        # cmd = "libcamera-jpeg -o " + INPUT_IMAGE_PATH + " -t 1000 --width 2500 --height 2500"
        if usecam:
            #cmd = "fswebcam -d /dev/video0  -v -S 60 --no-banner " + INPUT_IMAGE_PATH
            #p = self.create(cmd)
            #p.wait()
            capture(filename=INPUT_IMAGE_PATH)
            self.create("sudo mpg321 ./audios/camera_click.mp3")

        # Creating a scan of the input image
        img = cv2.imread(INPUT_IMAGE_PATH)

        if blurCheck(img):
            print("image is blurry")
            self.create("sudo mpg321 ./audios/blurry.mp3")
        doc_scan.scan(INPUT_IMAGE_PATH, OUTPUT_IMAGE_PATH)

        string = doc_ocr.ocr(imagePath=OUTPUT_IMAGE_PATH)
        if string.strip() == "": string = ""
        if(len(string) > 3):
            print(f"string = {string}")
            tts(string)
            if checkInternet():
                self.create(self.start_sound() + ";sudo mpg321 ./audios/tts.mp3;" + self.end_sound())
            else:
                self.create(self.start_sound() + ";sudo aplay ./audios/pico.wav;" + self.end_sound())

        else:
            print(f"No text detected")
            self.create("sudo mpg321 ./audios/noText.mp3")
        
    
    #for billboards and far away text
    def perform_scene_ocr(self):        
        if usecam:
  #          cmd = "fswebcam -d /dev/video0 -r 960x960 -v -S 10 --set brightness=100% --no-banner " + INPUT_IMAGE_PATH
 #           p = self.create(cmd)
#            p.wait()
            capture(filename=INPUT_IMAGE_PATH)
            self.create("sudo mpg321 ./audios/camera_click.mp3")


        string = scene_ocr.ocr()
        if(len(string) > 3):
            print(f"string = {string}")
            tts(string)
            if checkInternet():
                self.create(self.start_sound() + ";sudo mpg321 ./audios/tts.mp3;" + self.end_sound())
            else:
                self.create(self.start_sound() + ";sudo aplay ./audios/pico.wav;" + self.end_sound())
        else:
            print(f"No text detected")
            self.create("sudo mpg321 ./audios/noText.mp3")
    
    #describe a scene near you.
    def perform_scene_desc(self):        
        if usecam:
  #          cmd = "fswebcam -d /dev/video0 -r 960x960 -v -S 10 --set brightness=100% --no-banner " + INPUT_IMAGE_PATH
 #           p = self.create(cmd)
            capture(filename=INPUT_IMAGE_PATH,preprocess=False)
            self.create("sudo mpg321 ./audios/camera_click.mp3")

#            p.wait()
        print("going to describe scene now")
        string = scene_desc.describe(cv.imread(INPUT_IMAGE_PATH))
        print("Scene described")
        if(len(string) > 3):
            print(f"string = {string}")
            tts(string)
            if checkInternet():
                self.create(self.start_sound() + ";sudo mpg321 ./audios/tts.mp3;" + self.end_sound())
            else:
                self.create(self.start_sound() + ";sudo aplay ./audios/pico.wav;" + self.end_sound())
        else:
            print(f"No text detected")
            self.create("mpg321 ./audios/noText.mp3")

    def perform_cloud_ocr(self,regional = False):
        if checkInternet():
            if usecam:
                #cmd = "fswebcam -d /dev/video0 -r 2500x2500 -v -S 10 --set brightness=100% --no-banner " + INPUT_IMAGE_PATH
                #p = self.create(cmd)
                #p.wait()
                capture(filename=INPUT_IMAGE_PATH,preprocess=False)
                self.create("sudo mpg321 ./audios/camera_click.mp3")
            #cap = cv2.VideoCapture(0)
            #cap.set(cv2.CAP_PROP_FRAME_WIDTH,2592)
            #cap.set(cv2.CAP_PROP_FRAME_HEIGHT,1944)
            #ret, frame = cap.read()
            #img = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
            #cv2.imwrite(INPUT_IMAGE_PATH,img)
            #img = cv2.imread(INPUT_IMAGE_PATH)
            #check with pi4
            #if blurCheck(img):
            #    self.create("sudo mpg321 ./audios/blurry.mp3")
            string = cloud_ocr.ocr(INPUT_IMAGE_PATH)
            if(string and len(string) > 3):
                print(f"string = {string}")
                tts(string,lang=self.language if regional else "en")
                if checkInternet():
                    self.create(self.start_sound() + ";sudo mpg321 ./audios/tts.mp3;" + self.end_sound())
                else:
                    self.create(self.start_sound() + ";sudo aplay ./audios/pico.wav;" + self.end_sound())
            else:
                print(f"No text detected")
                self.create("sudo mpg321 ./audios/noText.mp3" if not regional else "sudo mpg321 ./audios/noText_{}.mp3".format(self.language))
        else:
            self.create("sudo mpg321 ./audios/no-internet.mp3")

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
        elif self.state == State.CloudOCR:
            self.currProc = Process(target=self.perform_cloud_ocr)
        elif self.state == State.RegionalCloudOCR:
            self.currProc = Process(target=self.perform_cloud_ocr(regional=True))

        self.currProc.start()
    
    def cancel(self):
        self.kill()
        if self.currProc.is_alive():
            self.currProc.terminate()
    
    def multibutton(self):
        if self.state == State.RegionalCloudOCR:
            langs = ['kn','ta','te','ml']
            ind = langs.index(self.language)
            ind = (ind + 1) % len(langs)
            self.language = langs[ind] 
            self.create(self.start_sound() + ";sudo aplay ./audios/langPrompt_{};".format(self.language) + self.end_sound())
            print("language changed in regional mode")
        else:
            if checkInternet():
                self.create(self.start_sound() + ";sudo mpg321 ./audios/tts.mp3;" + self.end_sound())
            else:
                self.create(self.start_sound() + ";sudo aplay ./audios/pico.wav;" + self.end_sound())
