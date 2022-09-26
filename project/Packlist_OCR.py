import cv2
from VideoShow import VideoShow
from VideoGet import VideoGet
from CountsPerSec import CountsPerSec
import pytesseract
import pdfplumber
import re
import pandas as pd
import winsound
from PyQt5 import QtCore, QtGui, QtWidgets
import time
import PacklistGUI
import sys

def putIterationsPerSec(frame, iterations_per_sec):
    """
    Add iterations per second text to lower-left corner of a frame.
    """

    cv2.putText(frame, "{:.0f} iterations/sec".format(iterations_per_sec),
        (10, 450), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255))
    return frame

class Packlist_OCR:

    def __init__(self, packlist):
        self.packlist = packlist

# packlist conversion to Pandas dataframe
    def packlist_conversion(self):
        text = ''

        with pdfplumber.open(self.packlist) as pdf:
            for page in pdf.pages:
                text += page.extract_text()

        good_row_re = re.compile(r'(^[A-Z]\d{3,5})')
        filtered_lst = []

        for row in text.split('\n'):
            if good_row_re.findall(row):
                filtered_lst.append([row.split()[1], row.split()[2], int(row.split()[-1])])

        self.df = pd.DataFrame(filtered_lst)
        self.df.columns = ["Project", "Part", "Ship Qty"]
        self.df['Receive Qty'] = 0
        
    def print_df(self):
        print(self.df)

# Check on Quantity to see if all correct values passed. Cross Reference actual Grand Total on Packlist
    def total_qty_check(self):
        Total = self.df['Ship Qty'].sum()
        print(Total)

    def export_df_xls(self):
        self.df.to_excel(r'project\packlist.xlsx', index = False)


# method to draw boxes and captured text on original image
    def box_on_frame(self, frm, gryfrm, gui_obj):
        pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
        boxes = pytesseract.image_to_data(gryfrm, config='--psm 6')
        self.part_number = '' 
        self.gui_obj = gui_obj
    
        for x,b in enumerate(boxes.splitlines()):
                if x != 0:
                    b = b.split()
                    if len(b) == 12:
                        x,y,w,h = int(b[6]),int(b[7]),int(b[8]),int(b[9])
                        cv2.rectangle(frm, (x, y), (w+x, h+y), (0, 255, 0), 1)
                        cv2.putText(frm, b[11],(x, y-3),cv2.FONT_HERSHEY_COMPLEX_SMALL,1,(50,50,255),1)
                        if re.match(r'([A-Z]{2}-\d{5,6})|(\d{6}-[A-Z]{2})|(TR6-[A-Z]{2})', b[11]) or re.match(r'(\s\d{6}\s)', b[11]) and len(b[11]) == 6:
                            self.part_number = b[11]
                            winsound.Beep(1800,100)

        if self.part_number != '':
            self.search_df_for_part_number()

    def search_df_for_part_number(self):
        if self.part_number not in self.df.values:
            invalid_part = '{} does not exist in the packlist'.format(self.part_number)
            self.gui_obj.update_label(invalid_part)
            QtWidgets.QApplication.processEvents()
            winsound.Beep(250,500)

        else:
            for index, row in self.df.iterrows():
                if row[1] == self.part_number:
                    if row[2] != row[3]:
                        self.df.at[index, "Receive Qty"] += 1
                        updated_qty = self.df.at[index, "Receive Qty"]
                        val_part = 'Index: {}     Project: {}     Part #: {}     Shipped Quantity: {}     Received Quantity: {}'.format(index, row[0], row[1], row[2], updated_qty)
                        self.gui_obj.update_label(val_part)
                        QtWidgets.QApplication.processEvents()
                        break
                    else:
                        if index == self.df.last_valid_index():
                            self.gui_obj.update_label('EXTRA PART!!!')
                            QtWidgets.QApplication.processEvents()
                        continue
                else:
                    if index == self.df.last_valid_index():
                            self.gui_obj.update_label('EXTRA PART!!!')
                            QtWidgets.QApplication.processEvents()

                    
# camera capture of part number from part label
    def video_capture(self, source = 1):

        # Initialize GUI 
        app = QtWidgets.QApplication(sys.argv)
        MainWindow = QtWidgets.QMainWindow()
        ui = PacklistGUI.Ui_MainWindow()
        ui.setupUi(MainWindow)
        MainWindow.show()
        

        # Video get and show threads
        video_getter = VideoGet(source).start()
        video_shower = VideoShow(video_getter.frame).start()
        cps = CountsPerSec().start()

        while True:
            QtWidgets.QApplication.processEvents()
            if video_getter.stopped or video_shower.stopped:
                video_shower.stop()
                video_getter.stop()
                break 

            frame = video_getter.frame

            # capture frame after n occurances to reduce lag in video code
            if cps._num_occurrences % 1000 == 0:
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                ret, thresh = cv2.threshold(gray, 210, 230, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)
                # self.box_on_frame(frame, thresh, ui)

            frame = putIterationsPerSec(frame, cps.countsPerSec())
            video_shower.frame = frame
            cps.increment() 

        cv2.destroyAllWindows()
        ui.stop(app)
 
# Create Desktop Application

if __name__ == "__main__":
    # import packlist file
    input = r'C:\Users\alanv\PythonCode\Projects\packlist OCR\project\126941.pdf'

    # instantiate Packlist_OCR object
    packlist = Packlist_OCR(input)
    packlist.packlist_conversion()
    # packlist.print_df()
    # packlist.total_qty_check()
    # packlist.export_df_xls()

    # While loop scanning label / displaying info / updating dataframe
    packlist.video_capture()