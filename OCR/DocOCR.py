import cv2
import pytesseract
from PIL import Image
#from DocScanner import DocScanner 





class DocOCR:
    
    def ocr(self,imagePath=None):
        
        image=cv2.imread(imagePath)
        
            
        #image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        #thresh_val, image = cv2.threshold(image, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        
        '''
        #comment this
        cv2.imshow("op",image)
        cv2.waitKey(0) # waits until a key is pressed
        #till here
        '''
        
        
        return pytesseract.image_to_string(image)
 
'''
img = cv2.imread('cell_pic.jpg')
_,scannedImage = DocScanner.scan(img=img)
resized_down = cv2.resize(scannedImage, (320,320), interpolation= cv2.INTER_LINEAR)
cv2.imshow("op",resized_down)
cv2.waitKey(0) # waits until a key is pressed

cv2.imwrite('output_image.jpg',scannedImage)
cv2.destroyAllWindows()
obj=DocOCR()
stri=obj.ocr(imagePath='output_image.jpg')
print(stri)
'''
