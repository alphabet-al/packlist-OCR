# Import required packages
import cv2
import pytesseract
import numpy as np

def biggest_contour(contours):
    biggest = np.array([])
    max_area = 0
    for i in contours:
        area = cv2.contourArea(i)
        if area > 1000:
            peri = cv2.arcLength(i, True)
            approx = cv2.approxPolyDP(i, 0.015 * peri, True)
            if area > max_area and len(approx) == 4:
                biggest = approx
                max_area = area
    return biggest
 
# Mention the installed location of Tesseract-OCR in your system
pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
 
# Read image from which text needs to be extracted
img = cv2.imread("project/label.jpg", cv2.IMREAD_REDUCED_COLOR_2)

img_original = img.copy()

# Convert the image to gray scale 
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
gray = cv2.bilateralFilter(gray, 20, 30, 30)
edged = cv2.Canny(gray, 100, 80)

contours, hierarcy = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
contours = sorted(contours, key = cv2.contourArea, reverse=True) [:10]

biggest = biggest_contour(contours)

cv2.drawContours(img, [biggest], -1, (0, 255, 0), 3)

points = biggest.reshape(4,2)
input_points = np.zeros((4, 2), dtype='float32')

points_sum = points.sum(axis=1)
input_points[0] = points[np.argmin(points_sum)]
input_points[3] = points[np.argmax(points_sum)]

points_diff = np.diff(points, axis = 1)
input_points[1] = points[np.argmin(points_diff)]
input_points[2] = points[np.argmax(points_diff)]

(top_left, top_right, bottom_right, bottom_left) = input_points
bottom_width = np.sqrt(((bottom_right[0] - bottom_left[0]) ** 2) + ((bottom_right[1] - bottom_left[1]) ** 2 ))
top_width = np.sqrt(((top_right[0] - top_left[0]) ** 2) + ((top_right[1] - top_left[1]) ** 2 ))
right_height = np.sqrt(((top_right[0] - bottom_right[0]) ** 2) + ((top_right[1] - bottom_right[1]) ** 2 ))
left_height = np.sqrt(((top_left[0] - bottom_left[0]) ** 2) + ((top_left[1] - bottom_left[1]) ** 2 ))

max_width = max(int(bottom_width), int(top_width))
max_height = max_width
# max_height = max(int(right_height), int(left_height))

converted_points = np.float32([[0,0], [max_width, 0], [0, max_height], [max_width, max_height]])

# Perspective transformation
matrix = cv2.getPerspectiveTransform(input_points, converted_points)
img_output = cv2.warpPerspective(img_original, matrix, (max_width, max_height))
resized = cv2.resize(img_output, (600, 600), interpolation = cv2.INTER_AREA)

gray = np.stack((gray,) * 3, axis = -1)
edged = np.stack((edged,) * 3, axis = -1)
img_hor = np.hstack((img_original, gray, edged, img))
cv2.imshow("Contour detection", img_hor)
cv2.imshow('Warped perspective', img_output)

cv2.imwrite('project/label_wp.jpg',resized)

cv2.waitKey(0)

