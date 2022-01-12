import os

import cv2
import imutils
import numpy as np
from imutils import perspective
from rembg.bg import remove as rembg

APPROX_POLY_DP_ACCURACY_RATIO = 0.02
IMG_RESIZE_H = 500.0

class DocScanner:
    def scan(self, img=None, imagePath=None):
        if img is not None:
            pass
        elif imagePath is not None:
            img = cv2.imread(imagePath)
        else:
            return None
        
        orig = img.copy()

        ratio = img.shape[0] / IMG_RESIZE_H

        img = imutils.resize(img, height=int(IMG_RESIZE_H))
        _, img = cv2.threshold(img[:,:,2], 0, 255, cv2.THRESH_BINARY)
        img = cv2.medianBlur(img, 15)

        cnts = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        cnts = sorted(cnts, key=cv2.contourArea, reverse=True)

        outline = None

        for c in cnts:
            perimeter = cv2.arcLength(c, True)
            polygon = cv2.approxPolyDP(c, APPROX_POLY_DP_ACCURACY_RATIO * perimeter, True)

            if len(polygon) == 4:
                outline = polygon.reshape(4, 2)

        r = orig
        if outline is not None:
            r = perspective.four_point_transform(orig, outline * ratio)
        else:
            print("yes")
        return r
    
if __name__ == "__main__":
    image = cv2.imread('cell_pic.jpg')
    scanned_image = DocScanner().scan(img=image)
    cv2.imwrite('scanned_image.jpg', scanned_image)