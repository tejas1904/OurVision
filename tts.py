from gtts import gTTS
import time

def tts(text):
    if len(text) < 3:
        return
    s = gTTS(text)
    s.save('tts.mp3')
    time.sleep(0.2)
