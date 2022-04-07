import cv2
import numpy as np

def rectify(h):
    h = h.reshape((4,2))
    hnew = np.zeros((4,2),dtype = np.float32)

    add = h.sum(1)
    hnew[0] = h[np.argmin(add)]
    hnew[2] = h[np.argmax(add)]

    diff = np.diff(h,axis = 1)
    hnew[1] = h[np.argmin(diff)]
    hnew[3] = h[np.argmax(diff)]

    return hnew

class Scanner(object):
    def __init__(self):
        pass
    def __del__(self):
        pass

    def auto_canny(self, image, sigma=0.33):
        v = np.median(image)
    
        lower = int(max(0, (1.0 - sigma) * v))
        upper = int(min(255, (1.0 + sigma) * v))
        edged = cv2.Canny(image, lower, upper)
    
        # return the edged image
        return edged

    # http://www.pyimagesearch.com/2014/08/25/4-point-opencv-getperspective-transform-example/
    def four_point_transform(self, image, rect):
    	# obtain a consistent order of the points and unpack them
        # individually
        (tl, tr, br, bl) = rect
    
        # compute the width of the new image, which will be the
        # maximum distance between bottom-right and bottom-left
        # x-coordiates or the top-right and top-left x-coordinates
        widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
        widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
        maxWidth = max(int(widthA), int(widthB))
    
        # compute the height of the new image, which will be the
        # maximum distance between the top-right and bottom-right
        # y-coordinates or the top-left and bottom-left y-coordinates
        heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
        heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
        maxHeight = max(int(heightA), int(heightB))
    
        # now that we have the dimensions of the new image, construct
        # the set of destination points to obtain a "birds eye view",
        # (i.e. top-down view) of the image, again specifying points
        # in the top-left, top-right, bottom-right, and bottom-left
        # order
        dst = np.array([
            [0, 0],
            [maxWidth - 1, 0],
            [maxWidth - 1, maxHeight - 1],
            [0, maxHeight - 1]], dtype = "float32")
    
        # compute the perspective transform matrix and then apply it
        M = cv2.getPerspectiveTransform(rect, dst)
        warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))
    
        # return the warped image
        return warped

    # https://github.com/vipul-sharma20/document-scanner
    def detect_edge(self, image, enabled_transform = False):
        dst = None
        orig = image.copy()

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        edged = cv2.Canny(blurred, 0, 20)
        _, contours = cv2.findContours(edged, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
        print(contours)
        contours = sorted(contours, key=cv2.contourArea, reverse=True)

        for cnt in contours:
            epsilon = 0.051 * cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, epsilon, True)

            if len(approx) == 4:
                target = approx
                cv2.drawContours(image, [target], -1, (0, 255, 0), 2)

                if enabled_transform:
                    approx = rectify(target)
                    # pts2 = np.float32([[0,0],[800,0],[800,800],[0,800]])
                    # M = cv2.getPerspectiveTransform(approx,pts2)
                    # dst = cv2.warpPerspective(orig,M,(800,800))
                    dst = self.four_point_transform(orig, approx)
                break

        return image, dst

if __name__ == "__main__":
	img = cv2.imread("camera_image_2.jpeg")
	cv2.imshow("", img)
	cv2.waitKey(0) # waits until a key is pressed
	cv2.destroyAllWindows()
	frame, _ = Scanner().detect_edge(img, enabled_transform=True)
	cv2.imshow("", frame)
