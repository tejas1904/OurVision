import cv2
import numpy as np 

class DocScanner:
    @classmethod
    def scan(self, img=None, path=None):
        if img is not None:
            pass
        elif path is not None:
            img = cv2.imread(path)
        else:
            print("no image detected...")

        height, width, _ = img.shape # Find Height And Width Of Image

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # RGB To Gray Scale

        kernel = np.ones((5, 5), np.uint8) # Reduce Noise Of Image
        erosion = cv2.erode(gray, kernel, iterations=1)
        opening = cv2.morphologyEx(erosion, cv2.MORPH_OPEN, kernel)
        closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)

        edges = cv2.Canny(closing, 20, 240) # Find Edges

        # Get Threshold Of Canny
        thresh = cv2.adaptiveThreshold(edges, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)  

        # Find Contours In Image
        contours, _ = cv2.findContours(thresh,cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)  

        # Find Biggest Contour
        areas = [cv2.contourArea(c) for c in contours]
        max_index = np.argmax(areas)

        # Find approxPoly Of Biggest Contour
        epsilon = 0.1 * cv2.arcLength(contours[max_index], True)
        approx = cv2.approxPolyDP(contours[max_index], epsilon, True)

        # Crop The Image To approxPoly
        try:
                pts1 = np.float32(approx)
                pts = np.float32([[0, 0], [width, 0], [width, height], [0, height]])
                matrix = cv2.getPerspectiveTransform(pts1, pts)
                result = cv2.warpPerspective(img, matrix, (width, height))

                flip = cv2.flip(result, 1) # Flip Image
                return 1, flip
        except:
                print("couldnt approximate poly");
                return 0, img

if __name__ == "__main__":    
    img = cv2.imread('receipt.jpg')
    _,scannedImage = DocScanner.scan(img=img)
    resized_down = cv2.resize(scannedImage, (320,320), interpolation= cv2.INTER_LINEAR)
    cv2.imshow("op",resized_down)
    cv2.waitKey(0) # waits until a key is pressed
    cv2.destroyAllWindows()
