import cv2
import pytesseract
from PIL import Image
from docscan.doc import scan

class DocOCR:
    def __init__(self, imagePath:str=None, image=None):
        if imagePath:
            self.imagePath:str=imagePath
            self.image=cv2.imread(imagePath)
        if image:
            self.image=image
        assert self.image is not None
        self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)

    def ocr(self) -> str:
        return pytesseract.image_to_string(self.image)
    