# Import required packages
import cv2
import pytesseract
import pdfplumber
import re
import pandas as pd
 
class Packlist_OCR:

    def __init__(self, packlist):
        self.packlist = packlist

    # packlist conversion to Pandas dataframe
    def packlist_conversion(self):
        text = ''

        with pdfplumber.open(self.packlist) as pdf:
            for page in pdf.pages:
                text += page.extract_text()

        good_row_re = re.compile(r'(^[A-Z]\d{5})')
        filtered_lst = []

        for row in text.split('\n'):
            if good_row_re.findall(row):
                filtered_lst.append([row.split()[1], row.split()[2], int(row.split()[-1])])

        self.df = pd.DataFrame(filtered_lst)
        self.df.columns = ["Project", "Part", "Qty"]
        self.df['Picked Qty'] = ''

    def print_df(self):
        print(self.df)

    def total_qty_check(self):

        # Check on Quantity to see if all correct values passed. Cross Reference actual Grand Total on Packlist
        
        Total = self.df['Qty'].sum()
        print(Total)

    def export_df_xls(self):
        self.df.to_excel(r'project\packlist.xlsx', index = False)

        

    # camera capture of part number from part label

    # display part number, project name and total quantity (tkinter?)

    # update dataframe after part number is scanned from label

    # create function to display items where picked quantity doesn't equal part quantity


# import packlist file

# instantiate Packlist_OCR object

# While loop scanning label / displaying info / updating dataframe

input = r'project\\90861.pdf'
packlist = Packlist_OCR(input)
packlist.packlist_conversion()
packlist.print_df()
packlist.total_qty_check()
packlist.export_df_xls()
