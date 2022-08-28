import pdfplumber
import re
import pandas as pd

input = r'project\\122135.pdf'

with pdfplumber.open(input) as pdf:
    page = pdf.pages[0]
    text = page.extract_text()

good_row_re = re.compile(r'\w+_')
filtered_lst = []

for row in text.split('\n'):
    if good_row_re.findall(row):
        filtered_lst.append([row.split()[1], row.split()[2], row.split()[-1]])

print(filtered_lst)

df = pd.DataFrame(filtered_lst)
df.columns = ["Project", "Part", "Qty"]

print(df)

