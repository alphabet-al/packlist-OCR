import cv2
import pytesseract
import re

def box_on_frame(frm, gryfrm):
    pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
    boxes = pytesseract.image_to_data(gryfrm)

    for x,b in enumerate(boxes.splitlines()):
            if x != 0:
                b = b.split()
                if len(b) == 12:
                    x,y,w,h = int(b[6]),int(b[7]),int(b[8]),int(b[9])
                    cv2.rectangle(frm, (x, y), (w+x, h+y), (0, 255, 0), 1)
                    cv2.putText(frm, b[11],(x, y-3),cv2.FONT_HERSHEY_COMPLEX_SMALL,1,(50,50,255),1)
                    if re.match(r'(\w{2}-\d{5,6})|(\d{6}-\w{2})|(TR6-\w{2})', b[11]) or re.match(r'(\d{6})', b[11]) and len(b[11]) == 6:
                        part_number = b[11]
                        print(part_number)
    
cap = cv2.VideoCapture(1)

# Check if the webcam is opened correctly
if not cap.isOpened():
    raise IOError("Cannot open webcam")

while True:
    _ , frame = cap.read()
    # frame = cv2.resize(frame, None, fx=2.0, fy=2.0, interpolation=cv2.INTER_AREA)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.bilateralFilter(gray, 20, 30, 30)

    box_on_frame(frame, gray)

    cv2.imshow('Input', frame)

    c = cv2.waitKey(1)
    if c == 27:
        break

cap.release()
cv2.destroyAllWindows()
