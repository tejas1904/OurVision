from subprocess import Popen

def play_audio(file):
    Popen("mpg321 " + file, shell=True).wait()