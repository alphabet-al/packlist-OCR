import pdfplumber
import re
import pandas as pd


input = r'project\\90861.pdf'
text = ''

with pdfplumber.open(input) as pdf:
    for page in pdf.pages:
        text += page.extract_text()

good_row_re = re.compile(r'(^[A-Z]\d{5})')
filtered_lst = []

for row in text.split('\n'):
    if good_row_re.findall(row):
        filtered_lst.append([row.split()[1], row.split()[2], int(row.split()[-1])])

print(filtered_lst)

df = pd.DataFrame(filtered_lst)
df.columns = ["Project", "Part", "Qty"]
df['Picked Qty'] = ''

dflist = ['Qty']
print(df)

# Check on Quantity to see if all correct values passed. Cross Reference actual Grand Total on Packlist
# Total = df['Qty'].sum()
# print(Total)

# export to excel file
# df.to_excel(r'project\packlist.xlsx', index = False)
