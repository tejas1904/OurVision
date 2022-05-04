import cv2 as cv

from paths import INPUT_IMAGE_PATH, TEXT_DETECTION_MODEL_PATH, TEXT_RECOGNITION_MODEL_PATH
from OCR import SceneOCR, DocScanner, DocOCR
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
Cloud_api_key="/home/pi/Desktop/OurVision/Api_Keys/ourvision-key.json"
cloud_ocr=CloudOCR("/home/pi/Desktop/OurVision/Api_Keys/ourvision-key.json")
