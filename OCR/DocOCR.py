import cv2
import pytesseract

class DocOCR:
    def ocr(self, imagePath=None):
        image = cv2.imread(imagePath)
        #image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        return pytesseract.image_to_string(image)
 

if __name__ == "__main__":
    img = cv2.imread('cell_pic.jpg')
    resized_down = cv2.resize(img, (320,320), interpolation= cv2.INTER_LINEAR)
    cv2.imshow("op",resized_down)
    cv2.waitKey(0) # waits until a key is pressed

    obj=DocOCR()
    stri=obj.ocr(imagePath='output_image.jpg')
    print(stri)
