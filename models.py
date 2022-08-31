import cv2 as cv

from paths import *

from OCR.SceneOCR import SceneOCR
from OCR.DocOCR import DocOCR
from OCR.DocScanner.scan import DocScanner
from OCR.CloudOCR import CloudOCR
from SceneDescribe.Depth import SceneDescribe

### SCENE OCR ###
detector_model = cv.dnn.readNet(TEXT_DETECTION_MODEL_PATH)
recognizer_model = cv.dnn.readNet(TEXT_RECOGNITION_MODEL_PATH)

scene_ocr=SceneOCR(detector_model,recognizer_model,INPUT_IMAGE_PATH)

### SCENE DESCRIBE ###
scene_desc=SceneDescribe(depth_model_path=DEPTH_MODEL_PATH, object_detection_model_path=OBJECT_DETECTION_MODEL_PATH)

### DOC OCR ###
doc_scan=DocScanner()
doc_ocr=DocOCR()

##CLOUD OCR##
cloud_ocr=CloudOCR(CLOUD_API_KEY)
