from gtts import gTTS
import time
import requests
from subprocess import Popen
import cv2
from googletrans import Translator
translator = Translator()


def checkInternet():
    try:
        _ = requests.head("http://www.google.com",timeout = 3)
        return True
    except: pass
    return False

def blurCheck(img):
    val = cv2.Laplacian(img,cv2.CV_64F).var()
    print("Variance of image is",val)
    return val < 100


def tts(text, lang = "en"):
    print("text is ", text)
    if not text : text = "No text Detected"
    if lang != "en":
        try:
            x = translator.translate(text,dest = lang)
            text = x.text
        except:
            text = "An Error Occured. Please try again or contact the developers."
            lang = "en"
    if checkInternet():
        if len(text) < 3:
            return
        s = gTTS(text,lang = lang)
        s.save('./audios/tts.mp3')
        time.sleep(0.2)
    else:
        cmd = "pico2wave --wave=./audios/pico.wav " + "\"" + text + "\""
        Popen(cmd,shell = True).wait()
        #player = "sudo aplay ./audios/pico.wav"
        #Popen(player,shell = True).wait()


