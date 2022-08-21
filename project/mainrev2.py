# Import required packages
import cv2
import pytesseract
 
# Mention the installed location of Tesseract-OCR in your system
pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
  
# Read image from which text needs to be extracted
img = cv2.imread("project/label_wp.jpg")
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# Convert the image to gray scale
# gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# cv2.imshow('gray image', gray)
# cv2.waitKey(0)

# Gaussian filtering of gray image
# blur = cv2.GaussianBlur(gray,(5,5),0)

# Performing OTSU threshold
# ret, thresh1 = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)
 
# Specify structure shape and kernel size.
# Kernel size increases or decreases the area
# of the rectangle to be detected.
# A smaller value like (10, 10) will detect
# # each word instead of a sentence.
# rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
 
# # Applying dilation on the threshold image
# dilation = cv2.dilate(thresh1, rect_kernel, iterations = 1) 
 
# # Finding contours
# contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL,
#                                                  cv2.CHAIN_APPROX_NONE)
 
# Creating a copy of image
im2 = img.copy()
 
# A text file is created and flushed
file = open("recognized.txt", "w+")
file.write("")
file.close()

# Looping through the identified contours
# Then rectangular part is cropped and passed on
# to pytesseract for extracting text from it
# Extracted text is then written into the text file
# for cnt in contours:
# x, y, w, h = cv2.boundingRect(cnt)
x,y,w,h = 85,373,35,30
# x,y,w,h = 155,16,200,17

# Drawing a rectangle on copied image
rect = cv2.rectangle(im2, (x, y), (x + w, y + h), (0, 255, 0), 2)
cv2.imshow("result", im2)
cv2.waitKey(0)
cv2.destroyAllWindows()
cv2.imwrite('project/result.jpg',im2)

# Cropping the text block for giving input to OCR
cropped = im2[y:y + h, x:x + w]
cv2.imshow('cropped', cropped)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Open the file in append mode
file = open("recognized.txt", "a")

# Apply OCR on the cropped image
text = pytesseract.image_to_string(cropped)

# Appending the text into file
file.write(text)
file.write("\n")

# Close the file
file.close 