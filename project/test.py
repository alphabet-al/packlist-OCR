import cv2
import imutils
import pytesseract
import numpy as np

def biggest_contour(contours):
    biggest = np.array([])
    max_area = 0
    for i in contours:
        area = cv2.contourArea(i)
        if area > 500:
            peri = cv2.arcLength(i, True)
            approx = cv2.approxPolyDP(i, 0.015 * peri, True)
            if area > max_area and len(approx) == 4:
                biggest = approx
                max_area = area

    return biggest

pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

image = cv2.imread(r'C:\Users\alanv\PythonCode\Projects\packlist OCR\project\label6.jpg')
image = imutils.resize(image, width = 450)
image_original = image.copy()
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray_image = cv2.bilateralFilter(gray_image, 11, 17, 17) 
edged = cv2.Canny(gray_image, 30, 200) 

cnts,new = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
image1=image.copy()
cv2.drawContours(image1,cnts,-1,(0,255,0),3)

cnts = sorted(cnts, key = cv2.contourArea, reverse = True) [:10]
screenCnt = None
image2 = image.copy()

biggest = biggest_contour(cnts)

try:
    cv2.drawContours(image2, [biggest], -1, (0, 255, 0), 3)
except:
    pass
 
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
img_output = cv2.warpPerspective(image_original, matrix, (max_width, max_height))

color = np.stack((gray_image,) * 3, axis = -1)
edged = np.stack((edged,) * 3, axis = -1)
img_hor = np.hstack((image2, edged, color, image))

new_img = img_output[74:92, 50:160]
cv2.imshow('cropped image', new_img)

# cv2.imshow("Contour detection", img_hor)
cv2.imshow('Warped perspective', img_output)
cv2.waitKey(0)

cv2.imwrite('project/label_wp.jpg',img_output)

strings = pytesseract.image_to_string(img_output, config='--psm 6')
print(strings)


# cv2.drawContours(image2,cnts,-1,(0,255,0),3)
# cv2.imshow('biggest contour', image2)
# cv2.imshow("Top 10 contours",image2)
# cv2.imshow("contours",image1)
# cv2.imshow("edged image", edged)
# cv2.imshow("smoothened image", gray_image)
# cv2.imshow("greyed image", gray_image)
# cv2.imshow('original image', image)
# cv2.waitKey(0)

