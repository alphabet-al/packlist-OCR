# Import required packages
import cv2
import pytesseract
import numpy as np
 
# Mention the installed location of Tesseract-OCR in your system
pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
 
# Read image from which text needs to be extracted
img = cv2.imread("project/resized.jpg")
img_original = img.copy()

# Convert the image to gray scale 
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
gray = cv2.bilateralFilter(gray, 20, 30, 30)
edged = cv2.Canny(gray, 10, 20)

gray = np.stack((gray,) * 3, axis = -1)
edged = np.stack((edged,) * 3, axis = -1)
img_hor = np.hstack((img_original, gray, edged))
cv2.imshow("Contour detection", img_hor)

cv2.waitKey(0)

