from ast import main
import cv2
 
def resize_image(img): 
    
    # print('Original Dimensions : ',img.shape)
    
    scale_percent = 60 # percent of original size
    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    dim = (width, height)
    
    # resize image
    resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
    # rrimage = cv2.rotate(resized, cv2.ROTATE_90_CLOCKWISE)
    
    # print('Resized Dimensions : ',resized.shape)
    
    # cv2.imshow("Original image", img) 
    # cv2.imshow("Resized image", resized)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    cv2.imwrite('project/resized.jpg',resized)

if __name__ == "__main__":
    img = cv2.imread('project/label.jpg', cv2.IMREAD_IGNORE_ORIENTATION)
    resize_image(img)