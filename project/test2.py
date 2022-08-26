# Import required packages
import cv2
import pytesseract
from PIL import Image, ExifTags

def check_image_orientation(img_path):

    try:
        image=Image.open(img_path)

        for orientation in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orientation]=='Orientation':
                break
        
        exif = image._getexif()

        if exif[orientation] == 3:
            image=image.rotate(180, expand=True)
        elif exif[orientation] == 6: 
            image=image.rotate(270, expand=True)
        elif exif[orientation] == 8:
            image=image.rotate(90, expand=True)

        image.save(img_path)
        image.close()
    except (AttributeError, KeyError, IndexError, TypeError):
        # cases: image don't have getexif
        pass

image_path = 'project/IMG_3162.jpg'
check_image_orientation(image_path)
pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
  
img = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
img = cv2.resize(img, (0,0), fx = 0.5, fy = 0.5)

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
gray = cv2.bilateralFilter(gray, 20, 30, 30)
edged = cv2.Canny(gray, 80, 100)

# cv2.imshow('orignial',img)
# cv2.imshow('gray', gray)
# cv2.imshow('edged', edged)
# cv2.waitKey(0)


hImg, wImg = edged.shape
boxes = pytesseract.image_to_data(img)
# print(boxes)

for x,b in enumerate(boxes.splitlines()):
    if x != 0:
        b = b.split()
        print(b)
        if len(b) == 12:
            x,y,w,h = int(b[6]),int(b[7]),int(b[8]),int(b[9])
            cv2.rectangle(img, (x, y), (w+x, h+y), (0, 255, 0), 1)
            cv2.putText(img, b[11],(x, y-3),cv2.FONT_HERSHEY_COMPLEX_SMALL,1,(50,50,255),1)
            if b[11] == 'DR-74467':
                part_number = b[11]

print(part_number)

cv2.imshow('Result',img)
cv2.waitKey(0)



