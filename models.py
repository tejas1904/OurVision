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
Depth_model_path="SceneDescribe/Models/lite-model_midas_v2_1_small_1_lite_1.tflite"
Object_detection_model_path="SceneDescribe/Models/efficientdet_lite0.tflite"

scene_desc=SceneDescribe(Depth_model_path , Object_detection_model_path)

### DOC OCR ###
doc_scan=DocScanner()
doc_ocr=DocOCR()

##CLOUD OCR##
cloud_ocr=CloudOCR(CLOUD_API_KEY)
