from time import sleep
from multiprocessing import Process
from subprocess import Popen
import pickle
import os
import signal

class PersistentList(list):
    def __init__(self, key, db):
        self.key = key
        self.extend(db.get(key, []))
    def _save(self):
        # db.set(self.key, self)
        print('saving {x}'.format(x = self))
    def __enter__(self):
        return self
    def __exit__(self,ext_type,exc_value,traceback):
        self._save()


class ShellProcess:
    def __init__(self, command, shell=False):
        self.p = None
        self.command = command
        self.shell = shell
        
    def start(self):
        self.p = Popen(self.command, shell=self.shell, preexec_fn=os.setpgrp)
        
    def terminate(self):
        if self.p:
            os.killpg(os.getpgid(self.p.pid), signal.SIGTERM)

class SubprocessObserver:
    def __init__(self):
        self.processes = []
    
    # Create a subprocess
    def create(self, command):
        p = Popen(command, shell=True, preexec_fn=os.setpgrp)
        
        # with open("test", "rb") as fp:   # Unpickling
        #     self.processes = pickle.load(fp)
        self.processes.append(p.pid)
        print(self.processes)
        pickle.dump(self.processes,open('test.p','wb'))

    
    # Kill and remove all the subprocesses
    def kill(self):
        self.processes = pickle.load(open('test.p', 'rb'))
        for pid in self.processes:
            os.killpg(os.getpgid(pid), signal.SIGTERM)
        self.processes = []
        
        # with open("test", "wb") as fp:   #Pickling
        #     pickle.dump(self.processes, fp)

class State:
    Count = 3
    DocOCR = 0
    SceneOCR = 1
    SceneDesc = 2
    
    @classmethod
    def name(cls, state):
        if state == State.DocOCR:
            return "DocOCR"
        if state == State.SceneOCR:
            return "SceneOCR"
        if state == State.SceneDesc:
            return "SceneDesc"
        return "Invalid"
        

class ButtonHandler:
    def __init__(self):
        self.state = State.DocOCR
        self.currProc = Process(target=self.performDocOcr, daemon=True)
        self.observer = SubprocessObserver()
        
    def create(self, command):
        self.observer.create(command)
        
    def performDocOcr(self):
        # how to create a subprocess
        self.create("python3 dococr.py")
    
    def performSceneOcr(self):
        self.create("python3 sceneocr.py")
    
    def performSceneDesc(self):
        self.create("python3 scenedesc.py")
    
    def kill(self):
        self.observer.kill()
        
    def cycle(self):
        self.state = (self.state + 1) % State.Count
        
    def select(self):
        if self.currProc.is_alive():
            return
        # self.kill()
        if self.state == State.DocOCR:
            self.currProc = Process(target=self.performDocOcr, daemon=True)
        elif self.state == State.SceneOCR:
            self.currProc = Process(target=self.performSceneOcr, daemon=True)
        elif self.state == State.SceneDesc:
            self.currProc = Process(target=self.performSceneDesc, daemon=True)

        self.currProc.start()
    
    def cancel(self):
        self.kill()
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

buttonHandler = ButtonHandler()

Test.cycleTest(buttonHandler)
Test.cycleTest(buttonHandler)
Test.cycleTest(buttonHandler)
    
Test.selectAndCancelTest(buttonHandler)
Test.selectAndCancelTest(buttonHandler)
Test.selectAndCancelTest(buttonHandler)

