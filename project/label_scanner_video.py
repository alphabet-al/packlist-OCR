# Import required packages
import cv2
import pytesseract
from PIL import Image, ExifTags
import re

cap = cv2.VideoCapture(1)

# Check if the webcam is opened correctly
if not cap.isOpened():
    raise IOError("Cannot open webcam")

while True:
    _ , frame = cap.read()
    cv2.imshow('Text detection', frame)
    if cv2.waitKey(1) & 0xFF == ord('s'):
        cv2.imwrite('project\capture_image.jpg', frame)
        break
cap.release()
cv2.destroyAllWindows()


image_path = 'project/capture_image.jpg'

pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
 
img = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
img = cv2.resize(img, (0,0), fx = 4.0, fy = 4.0)

# coverts image to grayscale, applys noise filter and edge detector
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# ret,thresh1 = cv2.threshold(gray,127,255,cv2.THRESH_BINARY)
ret, thresh1 = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)


boxes = pytesseract.image_to_data(thresh1)

for x,b in enumerate(boxes.splitlines()):
    if x != 0:
        b = b.split()
        if len(b) == 12:
            x,y,w,h = int(b[6]),int(b[7]),int(b[8]),int(b[9])
            cv2.rectangle(img, (x, y), (w+x, h+y), (0, 255, 0), 1)
            cv2.putText(img, b[11],(x, y-3),cv2.FONT_HERSHEY_SIMPLEX,1,(50,50,255),1)
            if re.match(r'(\w{2}-\d{5,6})|(\d{6}-\w{2})|(TR6-\w{2})', b[11]) or re.match(r'(\s\d{6}\s)', b[11]) and len(b[11]) == 6:
                part_number = b[11]
                print(part_number)
                
'''Shows original mage with boxes and text around captured text'''             
cv2.imshow('Result',img)
cv2.waitKey(0)





