from audio import play_audio

class State:
    Count = 5
    DocOCR = 0
    SceneOCR = 1
    SceneDesc = 2
    CloudOCR = 3
    RegionalCloudOCR = 4

     
    mp3dict={0:"DocumentOCRMode.mp3",1:"SceneOCRMode.mp3",2:"DescribeSceneMode.mp3", 3:"CloudOCRMode.mp3",4:"RegionalCloudOCRMode.mp3"}
    
    @classmethod
    def name(cls, state):
        if state == State.DocOCR:
            return "DocOCR"
        if state == State.SceneOCR:
            return "SceneOCR"
        if state == State.SceneDesc:
            return "SceneDesc"
        if state == State.CloudOCR:
            return "CloudOCR"
        if state == State.RegionalCloudOCR:
            return "RegionalCloudOCR"
        return "Invalid"
        
    @classmethod
    def play(cls, state):
        play_audio(State.mp3dict[state])
        
