from subprocess import Popen

def play_audio(file):
    Popen("mpg321 ./audios/" + file, shell=True).wait()