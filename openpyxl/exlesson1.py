import openpyxl as xl
excel_file = xl.load_workbook("Lear_openpyxl.xlsx")
sheet = excel_file.active
for row in sheet.iter_rows(values_only=True):
    print(row)