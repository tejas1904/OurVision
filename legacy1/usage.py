"""
You can start coding from ~ line 120. You can remove print statements - they are for debugging and tracking progress.
"""

"""
Requirements

matplotlib==3.2.2
numpy==1.18.5
ocrd-fork-pylsd==0.0.3
opencv-python==4.2.0.34
scipy==1.5.0

-> For Python 2/3

pip install matplotlib==3.2.2
pip install numpy==1.18.5
pip install ocrd-fork-pylsd==0.0.3
pip install opencv-python==4.2.0.34
pip install scipy==1.5.0

(or)

pip install matplotlib==3.2.2 numpy==1.18.5 ocrd-fork-pylsd==0.0.3 opencv-python==4.2.0.34 scipy==1.5.0

-> For Python 3

pip3 install matplotlib==3.2.2
pip3 install numpy==1.18.5
pip3 install ocrd-fork-pylsd==0.0.3
pip3 install opencv-python==4.2.0.34
pip3 install scipy==1.5.0

(or)

pip3 install matplotlib==3.2.2 numpy==1.18.5 ocrd-fork-pylsd==0.0.3 opencv-python==4.2.0.34 scipy==1.5.0

"""

import cv2
from PIL import Image
from scanner import DocScanner
import time

import pytesseract as pt
pt.pytesseract.tesseract_cmd = '/usr/bin/tesseract'

"""
OCR Function
Input - Scanned Image
Output - OCR'ed String
"""

def ocr(image):
    a = pt.image_to_string(image)

    lines = a.split("\n")
    newLines = []
    for i in lines:
        if i != ' ' and i != '  ' and i != '   ' and i != '' and i != "    ":
            newLines.append(i)
            
    finalString = ""
    for i in newLines:
        finalString += i + ".\n"
        
    return finalString
"""
End of OCR Function
"""

"""
Do Image Processing with the scanned_image

For E.g.,
1. enhance the image
2. increase contrast
3. use canny, sobel
4. use thresholding
5. use morpho dilation, erosion

If nothing, atleast use this:

Input - np.array (image)
Output - PIL.Image - compatible with ocr()
"""

def image_processing(image):
    from PIL import Image, ImageEnhance, ImageFilter

    #read the image
    im = Image.fromarray(image)
    print("3.1 extracted image")

    enhancer = ImageEnhance.Contrast(im)

    factor = 1 #gives original image
    im_output = enhancer.enhance(factor)
    print("3.2 enhanced image")

    factor = 0.5 #decrease constrast
    im_output = enhancer.enhance(factor)
    print("3.3 decreased contrast")

    factor = 1.5 #increase contrast
    im_output = enhancer.enhance(factor)
    print("3.4 increased contrast")


    x = im.convert('L')
    im_output = x.point(lambda x: 0 if x<128 else 255, '1')
    print("3.5 segmented image")
    
    #im_output.filter(ImageFilter.MinFilter(25))
    #im_output.filter(ImageFilter.MaxFilter(9))
    print("3.6 image dilated and eroded")
    return im_output

"""
Start your logic
"""
startTime = time.time()

# read the image
image = cv2.imread('cell_pic.jpg')

print("1. image read")

# scan the image
scanned_image = DocScanner().scan(image)

print("2. image scanned")

#resized it only for imshow
#resized_scanned_image = cv2.resize(scanned_image, (500, 750))
#cv2.imshow('Output Image', resized_scanned_image)
#cv2.waitKey(0)

processed_scanned_image = image_processing(scanned_image)

print("3. image processed")

executionTime = (time.time() - startTime)
print('Execution time in seconds: ' + str(executionTime))


ocr_string = ocr(processed_scanned_image)

print("4. image ocr'ed")

print("\n\n\n OCR String:\n")

print(ocr_string)

# text to speech here