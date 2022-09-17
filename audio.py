from subprocess import Popen

def play_audio(file):
    if file[-3:] == "wav":
        Popen("aplay ./audios/" + file, shell = True).wait()
    else:
        Popen("mpg321 ./audios/" + file, shell=True).wait()