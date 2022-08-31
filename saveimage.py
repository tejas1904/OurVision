
import cv2
import time
import numpy as np
def main():
    capture = capture_write()


def capture_write(filename="image.jpeg", port=0, ramp_frames=30, x=1191, y=2000,preprocess=True):
    camera = cv2.VideoCapture(port)

    # Set Resolution
    camera.set(3, x)
    camera.set(4, y)

    # Adjust camera lighting
    for i in range(ramp_frames):
        temp = camera.read()
    retval, im = camera.read()
    cv2.imwrite(filename,im)
    del(camera)
    print("image Taken")

    if preprocess:
        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

    # Remove shadows, cf. https://stackoverflow.com/a/44752405/11089932
        dilated_img = cv2.dilate(gray, np.ones((3, 3), np.uint8))
        bg_img = cv2.medianBlur(dilated_img, 25)
        diff_img = 255 - cv2.absdiff(gray, bg_img)
        norm_img = cv2.normalize(diff_img, None, alpha=0, beta=255,norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8UC1)

    # Threshold using Otsu's
        work_img = cv2.threshold(norm_img, 0, 255, cv2.THRESH_OTSU)[1]
        cv2.imwrite(filename,work_img)
        print("processed image saved")
    return True

if __name__ == '__main__':
    main()
