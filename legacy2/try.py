import pyttsx3

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('rate', 125)    
i=3
print(3)
engine.setProperty('voice', voices[i].id)
engine.say("now in doc scan mode")
engine.runAndWait()
