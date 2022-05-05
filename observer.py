import pickle
from subprocess import Popen
import signal
import os

class SubprocessObserver:
    def __init__(self):
        self.processes = []
        pickle.dump(self.processes, open('test.p', 'wb'))
    
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